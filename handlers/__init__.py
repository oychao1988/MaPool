#coding:utf-8

from handlers.mianfeisms_handler import MianfeismsHandler


class ApiServer:

    handlers = [MianfeismsHandler()]
    
    urls = [i for x in handlers for i in x.urls]


