import requests
import os
import re
import time
import socket

#  1. 文件夹创建遇到问题，删除特殊字符,   简化为一个for循环
#  2. 将一些简写的变量名改为有具体意思的名字
#  3. 用户可以自己在控制台输入想要从哪章那页开始爬取
#  4. 发现跳章爬取的逻辑问题，并修改

url = "https://m.36mh.com/manhua/tongjunanguimi/"
head = { "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Mobile Safari/537.36" }
path = '/同居男闺蜜/'

# 超时参数
socket.setdefaulttimeout(20)

# 获取网页源代码
r = requests.get(url,headers=head)
r.encoding = "utf-8"
HTML = ','.join(r.text.split())

htms_Value = re.findall(r"http://m.36mh.com/manhua/tongjunanguimi/\d{6}.html", HTML,re.M)
htms_key = re.findall(r"<span>(.*?)</span>",','.join(re.findall(r"<span>第.*?</span>", HTML,re.M)) ,re.M)

# 第几话的第几页开始爬取
# 上次截止为：19 12
End_Chapter = eval(input("请输入你要从第几章开始爬取："))
End_Page = eval(input("请输入你要从第"+str(End_Chapter)+"的第几页开始开始爬取："))

for item,Start_Chapter in zip(htms_Value,range(len(htms_Value))):

    if End_Chapter > Start_Chapter:
        continue
    print("》》》准备扒取：" + str(Start_Chapter) + htms_key[Start_Chapter])

    # 删除特殊字符
    for e in ["\\n","\\t","\\r","/","\\",":","*","\"","<",">","|","?"]:
        htms_key[Start_Chapter] = htms_key[Start_Chapter].replace(e,"")

    if (os.path.exists(path + str(Start_Chapter) + htms_key[Start_Chapter])):
        flag = 1
    else:
        os.makedirs(path + str(Start_Chapter) + htms_key[Start_Chapter])
        flag = 0
    os.chdir(path + str(Start_Chapter) + htms_key[Start_Chapter])

    r = requests.get(item,headers=head)
    r.encoding = "utf-8"
    HTML = ','.join(r.text.split())
    HTML1 = HTML
    count = eval(''.join(re.findall(r'<span,id="k_total",class="curPage">(.*?)</span>', HTML1, re.M)))
    print("本话共有："+str(count)+"张漫画")

    for Start_Page in range(count+1):
        if End_Page > Start_Page:
            continue
        else:
            End_Page = 0

        if Start_Page == 0:
            continue
        elif Start_Page == 1:
            htms_Value = re.findall(r'<mip-img,src="(.*?)">,', HTML, re.M)
        else:
            url = re.findall(r'^(.*?).html', item, re.M)[0]+"-"+str(Start_Page)+".html"
            r = requests.get(url,headers=head)
            r.encoding = "utf-8"
            HTML = ','.join(r.text.split())
            HTML1 = HTML
            htms_Value = re.findall(r'<mip-img,src="(.*?)">,', HTML, re.M)
        print("正在扒取第"+str(Start_Page)+"页...")
        time.sleep(1)
        r = requests.get(htms_Value[0],headers=head)
        f = open("./%s" % Start_Page + ".jpg", "wb")
        f.write(r.content)
        f.close()

    if count>50:
        print("30秒后自动开始爬取下一话")
        time.sleep(30)

print("结束")