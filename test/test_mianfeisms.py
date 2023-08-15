import re
from playwright.sync_api import Playwright, sync_playwright


def test_mianfeisms_phone_query(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    url_page = 1
    url_pattern = "https://www.mianfeisms.xyz/cn.php?page={page}"
    phone_nums = []
    while True:
        url = url_pattern.format(page=url_page)
        print(f"打开页面：{url}")
        page.goto(url)
        page.wait_for_load_state()
        items = page.get_by_role("heading", name=re.compile("\+\d+"))
        phone_nums.extend(items.all_inner_texts())
        max_page = page.locator('//ul[@class="pagination"]/li').last.inner_text()
        if url_page < int(max_page):
            url_page += 1
        else:
            break
    print(phone_nums)
    context.close()
    browser.close()

def test_mianfeisms_phone_code_fetch(playwright: Playwright, phone, name_pattern, code_length):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    url_pattern = "https://www.mianfeisms.xyz/sms.php?p={phone}"
    message_list = []
    url = url_pattern.format(phone=phone)
    print(f"打开页面：{url}")
    page.goto(url)
    page.wait_for_load_state()
    elements = page.locator('//div[@class="rowbox message_details"]')
    for i in range(elements.count()):
        if not elements.nth(i).inner_text():
            continue
        message_list.append({
            "from": elements.nth(i).locator("//div[@class='col-md-3 sender']").inner_text(),
            "message": elements.nth(i).locator("//div[@class='col-md-6 msg']").inner_text(),
            "time": elements.nth(i).locator("//div[@class='col-md-3 time']").inner_text(),
        })
    print(message_list)
    matched_list = list(filter(lambda x: re.findall(name_pattern, x["message"]), message_list))
    [each.update({"code": re.findall(f"\d{{{code_length}}}", each["message"])}) for each in matched_list]
    
    print(matched_list)
    context.close()
    browser.close()


# with sync_playwright() as playwright:
#     test_mianfeisms_phone_query(playwright=playwright)

with sync_playwright() as playwright:
    test_mianfeisms_phone_code_fetch(
        playwright=playwright, 
        phone="15938883624", 
        name_pattern="平安口袋银行",
        code_length=4
    )