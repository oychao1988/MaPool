import logging
import tornado.web
from tornado.web import url
from crawlers.mianfeisms_crawler import MianfeismsCrawler


Headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
}

class BaseHandler:
    '''内置基类'''


class MianfeismsHandler(BaseHandler):
    '''
    https://www.mianfeisms.xyz/ 的接码平台号码爬虫 及路由
    '''

    Server = '/mianfeisms'
    crawler = MianfeismsCrawler()
    logger = logging.getLogger()

    class GetCodesHandler(tornado.web.RequestHandler):
        
        async def get(self, *args, **kwargs):
            # 解析参数
            phone = self.get_argument("phone")
            name_pattern = self.get_argument("name_pattern")
            code_length = self.get_argument("code_length", 6)
            # 获取数据
            matched_list = await MianfeismsHandler.crawler.get_codes(phone, name_pattern, code_length)
            # 返回结果
            self.write({
                'success':0,
                'data': matched_list,
            })

    class GetPhonesHandler(tornado.web.RequestHandler):

        async def get(self, *args, **kwargs):
            """
            area_dict = {"cn": "china", "index": "usa", "gb": "uk", "hk": "hk"}
            """
            # 参数解析
            area = self.get_argument("area", "cn")
            start_page = int(self.get_argument("page", 1))
            pages = int(self.get_argument("pages", 10))
            # 获取数据
            phone_list = await MianfeismsHandler.crawler.get_phones(area, start_page, pages)
            # 返回结果
            self.write({
                'success': 0,
                'data': {
                    "code": MianfeismsHandler.crawler.area_dict[area]["code"],
                    "area": MianfeismsHandler.crawler.area_dict[area]["name"],
                    "phones": phone_list,
                    "total": len(phone_list)
                }
            })

    urls = [
        url(Server+'/fetch', GetCodesHandler, name='mianfeisms_phone_code_fetch'),
        url(Server+'/phone', GetPhonesHandler, name='mianfeisms_phone_query'),
    ]






