import re
import os
import logging
import json
import datetime
from playwright.async_api import async_playwright
from config import BASE_DIR


class BaseCrawler:
    '''内置基类'''


class MianfeismsCrawler(BaseCrawler):
    '''
    https://www.mianfeisms.xyz/ 的接码平台号码爬虫 及路由
    '''
    def __init__(self):
        self.area_dict = {
            "cn": {"name": "China", "code": "86"}, 
            "index": {"name": "USA", "code": "1"},  
            "gb": {"name": "UK", "code": "44"}, 
            "hk": {"name": "HK(China)", "code": "85"}
        }
        self.host = "https://www.mianfeisms.xyz"
        self.logger = logging.getLogger()

    async def get_codes(self, phone, name_pattern, code_length):
        url = self.host + f"/sms.php?p={phone}"

        message_list = []
        # 抓取数据
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            self.logger.info(f"打开页面：{url}")
            await page.goto(url)
            await page.wait_for_load_state()
            elements = page.locator('//div[@class="rowbox message_details"]')
            for i in range(await elements.count()):
                if not await elements.nth(i).inner_text():
                    continue
                message_list.append({
                    "from": await elements.nth(i).locator("//div[@class='col-md-3 sender']").inner_text(),
                    "message": await elements.nth(i).locator("//div[@class='col-md-6 msg']").inner_text(),
                    "time": await elements.nth(i).locator("//div[@class='col-md-3 time']").inner_text(),
                })
            await context.close()
            await browser.close()

        matched_list = list(filter(lambda x: re.findall(name_pattern, x["message"]), message_list))
        [each.update({"code": re.findall(f"\d{{{code_length}}}", each["message"])}) for each in matched_list]
        return matched_list

    async def get_phones(self, area, start_page, pages):
        phone_list = []
        url_pattern = self.host + "/{area}.php?page={page}"

        date = datetime.datetime.now().strftime("%Y%m%d")
        file_name = os.path.join(BASE_DIR, "datas", f"{area}_phones_{date}.json")

        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                phone_list = json.loads(f.read())
        else:
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                count = 0
                while count < pages:
                    url = url_pattern.format(area=area, page=start_page)
                    self.logger.info(f"打开页面：{url}")
                    await page.goto(url)
                    await page.wait_for_load_state()
                    # 获取当前页面的号码
                    items = page.get_by_role("heading", name=re.compile("\+\d+"))
                    phone_list.extend(await items.all_inner_texts())
                    # 获取分页器的最大页码
                    max_page = await page.locator('//ul[@class="pagination"]/li').last.inner_text()
                    if start_page < int(max_page):
                        start_page += 1
                    else:
                        break
                    count += 1
                self.logger.info("结束获取")
                await context.close()
                await browser.close()

            # 保存电话号码
            with open(file_name, "w") as f:
                f.write(json.dumps(phone_list))
        return phone_list