# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
#wydomain

import time
import json

from lib.captcha import Captcha
from lib.common import is_domain
from lib.log import logger

import requests
req = requests.Session()

class Chaxunla(object):
    """docstring for Chaxunla"""
    def __init__(self, domain, proxy=None):
        super(Chaxunla, self).__init__()
        self.domain = domain
        self.url = 'http://api.chaxun.la/toolsAPI/getDomain/'
        self.domain_name = []
        self.smiliar_domain_name = []
        self.email = []
        self.verify = ""
        self.engine_name= "Chaxunla"
        self.print_banner()
        return

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def run(self):
        try:
            timestemp = time.time()
            url = "{0}?0.{1}&callback=&k={2}&page=1&order=default&sort=desc&action=moreson&_={3}&verify={4}".format(
                self.url, timestemp, self.domain, timestemp, self.verify)
            result = json.loads(req.get(url).content)
            if result.get('status') == '1':
                for item in result.get('data'):
                    if is_domain(item.get('domain')):
                        self.domain_name.append(item.get('domain'))
            elif result.get('status') == 3:
                logger.warning("chaxun.la api block our ip...")
                logger.info("input you verify_code")
                # print('get verify_code():', self.verify)
                # self.verify_code()
                # self.run()
            self.domain_name = list(set(self.domain_name))
        except Exception as e:
            logger.info(str(e))
        finally:
            logger.info("{0} found {1} domains".format(self.engine_name, len(self.domain_name)))
            return self.domain_name,self.smiliar_domain_name,self.email


    def download(self, url):
        try:
            r = req.get(url)
            with open("captcha.gif", "wb") as image:
                image.write(r.content)
            return True
        except Exception, e:
            return False

    def verify_code(self):
        timestemp = time.time()
        imgurl = 'http://api.chaxun.la/api/seccode/?0.{0}'.format(timestemp)
        if self.download(imgurl):
            captcha = Captcha()
            code_result = captcha.verification(filename='captcha.gif')
            self.verify = code_result.get('Result')


if __name__ == "__main__":
        x = Chaxunla("meizu.com",proxy="http://127.0.0.1:9999")
        print  x.run()
