# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import re
import random
import time
from bs4 import BeautifulSoup
import pandas as pd
from requests_html2 import HTMLSession
import os, xlwt, xlrd, random
from xlutils.copy import copy
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties  # 字体库
from lxml import etree
from useragent import USER_AGENT_LIST

url = 'http://fund.eastmoney.com/fund.html'

def save_data(data_dict):
	file_dir_path = os.getcwd() + '/data/'
	if not os.path.exists(file_dir_path):
		print('create file path:{}'.format(file_dir_path))
		os.mkdir(file_dir_path)
	
	current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
	file_path = file_dir_path + 'fund_data' + current_time +'.xls'

	workbook = xlwt.Workbook(encoding='utf-8')
	worksheet = workbook.add_sheet('data', cell_overwrite_ok=True)
	title_list = ('基金名称', '昨日单位净值'， '昨日累计净值', '前日单位净值'， '前日累计净值', '日增长值', '日增长率')
	for i in range(len(title_list):
		worksheet.write(0, i, title_list[i])

	

	workbook.save(file_path)

def etree_t1():
    session = HTMLSession()
    headers = {'User-Agent': random.choice(USER_AGENT_LIST)}
    response = session.get(url, headers=headers).content
    """序列化对象，将字节内容数据，经过转换，变成可进行xpath操作的对象"""
    response_1 = etree.HTML(response)
    print(response_1)
    # 基金名称
    name_list = response_1.xpath('//tbody/tr/td[5]/nobr/a[1]/text()')
    print(name_list)
    # 昨日单位净值
    yesterday_value_list = response_1.xpath('//tbody/tr/td[6]/text()')
    print(yesterday_value_list)
    # 昨日累计净值
    yesterday_acc_value_list = response_1.xpath('//tbody/tr/td[7]/text()')
    print(yesterday_acc_value_list)
    # 前天单位净值
    yesterday_before_value_list = response_1.xpath('//tbody/tr/td[8]/text()')
    print(yesterday_before_value_list)
    # 前天累计净值
    yesterday_before_acc_value_list = response_1.xpath('//tbody/tr/td[9]/text()')
    print(yesterday_before_acc_value_list)
    # 日增长值
    acc_value_list = response_1.xpath('//tbody/tr/td[10]/text()')
    print(acc_value_list)
    # 日增长率
    acc_rate_list = response_1.xpath('//tbody/tr/td[11]/text()')
    print(acc_rate_list)

if __name__ == '__main__':
    etree_t1()
