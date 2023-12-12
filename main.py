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
from operator import attrgetter

url = 'http://fund.eastmoney.com/fund.html'
file_dir_path = os.getcwd() + '/data/'
current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())

class FundInfo:
    def __init__(self):
        self.fund_name = ''
        self.yesterday_value = 0.0
        self.yesterday_acc_value = 0.0
        self.yesterday_before_value = 0.0
        self.yesterday_before_acc_value = 0.0
        self.acc_val = 0.0
        self.acc_rate = 0.0

def parse_response(response):
    # 基金名称
    name_list = response.xpath('//tbody/tr/td[5]/nobr/a[1]/text()')
    print(name_list)
    # 昨日单位净值
    yesterday_value_list = response.xpath('//tbody/tr/td[6]/text()')
    print(yesterday_value_list)
    # 昨日累计净值
    yesterday_acc_value_list = response.xpath('//tbody/tr/td[7]/text()')
    print(yesterday_acc_value_list)
    # 前天单位净值
    yesterday_before_value_list = response.xpath('//tbody/tr/td[8]/text()')
    print(yesterday_before_value_list)
    # 前天累计净值
    yesterday_before_acc_value_list = response.xpath('//tbody/tr/td[9]/text()')
    print(yesterday_before_acc_value_list)
    # 日增长值
    acc_value_list = response.xpath('//tbody/tr/td[10]/text()')
    print(acc_value_list)
    # 日增长率
    acc_rate_list = response.xpath('//tbody/tr/td[11]/text()')
    print(acc_rate_list)

    fund_info_list = []
    zipped = zip(name_list, yesterday_value_list, yesterday_acc_value_list, \
                 yesterday_before_value_list, yesterday_before_acc_value_list, acc_value_list, acc_rate_list)
    for fund_name, yesterday_value, yesterday_acc_value, yesterday_before_value, \
            yesterday_before_acc_value, acc_val, acc_rate in zipped:
        fund_info = FundInfo()
        fund_info.fund_name = fund_name
        fund_info.yesterday_value = yesterday_value
        fund_info.yesterday_acc_value = yesterday_acc_value
        fund_info.yesterday_before_value = yesterday_before_value
        fund_info.yesterday_before_acc_value = yesterday_before_acc_value
        fund_info.acc_val = acc_val
        fund_info.acc_rate = acc_rate
        fund_info_list.append(fund_info)
    return fund_info_list

def save_data(fund_info_list):
    if not os.path.exists(file_dir_path):
        print('create file path:{}'.format(file_dir_path))
        os.mkdir(file_dir_path)

    file_path = file_dir_path + 'fund_data_' + current_time +'.xls'

    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('data', cell_overwrite_ok=True)
    title_list = ('基金名称', '昨日单位净值', '昨日累计净值', '前日单位净值', '前日累计净值', '日增长值', '日增长率')
    for i in range(0, len(title_list)):
        worksheet.write(0, i, title_list[i])
    nrow = 1
    for fund_info in fund_info_list:
        worksheet.write(nrow, 0, fund_info.fund_name)
        worksheet.write(nrow, 1, fund_info.yesterday_value)
        worksheet.write(nrow, 2, fund_info.yesterday_acc_value)
        worksheet.write(nrow, 3, fund_info.yesterday_before_value)
        worksheet.write(nrow, 4, fund_info.yesterday_before_acc_value)
        worksheet.write(nrow, 5, fund_info.acc_val)
        worksheet.write(nrow, 6, fund_info.acc_rate)
        nrow = nrow + 1
    print('collect fund num:{}'.format(nrow - 1))

    workbook.save(file_path)
    print('save fund data to xls.')

def draw_img(fund_info_list):
    # matplotlib.use('TkAgg')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 涨幅前10名
    top_ten_acc_list = fund_info_list[0: 10]
    x_array_name = [info.fund_name for info in top_ten_acc_list]
    x_array = range(1, 11)
    y_array = [info.acc_rate for info in top_ten_acc_list]
    plt.bar(x_array, y_array, width=0.5, color='steelblue', tick_label=x_array_name, label='日增长率')
    plt.xticks(rotation = -80)
    plt.title('日增长率Top10')
    plt.legend(loc='upper center')
    plt.gcf().subplots_adjust(bottom=0.4)
    file_dir = file_dir_path + '日增长率Top10柱状图_' + current_time + '.png'
    plt.savefig(file_dir)
    print('create acc rate top 10 funds.')
    plt.show()

    #净值前10名
    val_sort_list = sorted(fund_info_list, key=attrgetter('yesterday_value'), reverse=True)
    top_ten_val_list = val_sort_list[0: 10]
    x_array_name = [info.fund_name for info in top_ten_val_list]
    x_array = range(1, 11)
    y_array = [info.yesterday_value for info in top_ten_val_list]
    plt.bar(x_array, y_array, width=0.5, color='red', tick_label=x_array_name, label='日增长率')
    plt.xticks(rotation=-80)
    plt.title('日净值Top10')
    plt.legend(loc='upper center')
    plt.gcf().subplots_adjust(bottom=0.4)
    file_dir = file_dir_path + '日净值Top10柱状图_' + current_time + '.png'
    plt.savefig(file_dir)
    print('create value top 10 funds.')
    plt.show()

def crawl_func():
    session = HTMLSession()
    headers = {'User-Agent': random.choice(USER_AGENT_LIST)}
    response = session.get(url, headers=headers).content
    response_1 = etree.HTML(response)
    print(response_1)
    # 解析数据
    fund_info_list = parse_response(response_1)
    # 写xls文件
    save_data(fund_info_list)
    # 绘图
    draw_img(fund_info_list)

if __name__ == '__main__':
    crawl_func()
