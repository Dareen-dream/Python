import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from lxml import etree
import csv

url = 'https://www.zhipin.com/beijing/'
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
browser = webdriver.Chrome(options=option)
#访问
browser.get(url)

browser.maximize_window()

#文本输入
# browser.find_element_by_xpath('//*[@id="wrap"]/div[3]/div/div/div[1]/form/div[2]/p/input').send_keys('测试')
browser.find_element_by_xpath('//*[@id="wrap"]/div[4]/div/div/div[1]/form/div[2]/p/input').send_keys('测试')

# browser.find_element_by_xpath('//*[@id="wrap"]/div[3]/div/div/div[1]/form/button').click()
browser.find_element_by_xpath('//*[@id="wrap"]/div[4]/div/div/div[1]/form/button').click()
# //*[@id="wrap"]/div[2]/div/div/div[1]/form/div[2]/p/input

#翻页
# if browser.page_source.find('pn-next disabled') == -1:
#     # browser.find_element_by_xpath('//*[@id="J_bottomPage"]/span[1]/a[4]')
#     browser.find_element_by_class_name('pn-next').click()
# if browser.page_source.find('next disabled') == -1:
#     browser.find_element_by_xpath('//*[@id="main"]/div/div[3]/div[3]/a[5]')
#     # browser.find_element_by_class_name('next').click()

# #获取源码
# html = browser.page_source
# # print(html)
#
# li_list = browser.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li')
# for li in li_list:
#     # print(li)
#     goods_data = li.text.split('\n')
#     # print(goods_data)
#     goods_price = goods_data[0]
#
#     if '￥' in goods_data[1]:
#         goods_name = goods_data[2]
#         goods_comment = goods_data[3]
#         shop = goods_data[4]
#     else:
#         goods_name = goods_data[1]
#         goods_comment = goods_data[2]
#         shop = goods_data[3]
#     print(goods_price,goods_name,goods_comment,shop)
#
# #数据存储
# with open('Jd_goods.csv','w',newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(['价格','商品名','评价人数','店铺名'])
#     for li in li_list:
#         goods_data = li.text.split('\n')
#
#         goods_price = goods_data[0]
#
#         if '￥' in goods_data[1]:
#             goods_name = goods_data[2]
#             goods_comment = goods_data[3]
#             shop = goods_data[4]
#         else:
#             goods_name = goods_data[1]
#             goods_comment = goods_data[2]
#             shop = goods_data[3]
#
#         writer.writerow([goods_price,goods_name,goods_comment,shop])
#
#
# time.sleep(2)
#
# browser.quit()