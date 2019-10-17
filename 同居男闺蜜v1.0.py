import requests
import os
import re
import time
import socket
#添加了爬取等待时间，防止被认为是爬虫，而被断开连接
url = "https://m.36mh.com/manhua/tongjunanguimi/"
path = '/同居男闺蜜/'

socket.setdefaulttimeout(20)

r = requests.get(url)
r.encoding = "utf-8"
HTML = r.text
HTML = HTML.split()
HTML = ','.join(HTML)

htms_Value = re.findall(r"http://m.36mh.com/manhua/tongjunanguimi/\d{6}.html", HTML,re.M)
htms_key = re.findall(r"<span>(.*?)</span>",','.join(re.findall(r"<span>第.*?</span>", HTML,re.M)) ,re.M)
i = 0
for item in htms_Value:
    print("》》》准备扒取：" + htms_key[i])
    if (os.path.exists(path + htms_key[i])):
        flag = 1
    else:
        os.makedirs(path + htms_key[i])
        flag = 0
    os.chdir(path + htms_key[i])

    r = requests.get(item)
    r.encoding = "utf-8"
    HTML = r.text
    HTML = HTML.split()
    HTML = ','.join(HTML)
    HTML1 = HTML
    count = eval(''.join(re.findall(r'<span,id="k_total",class="curPage">(.*?)</span>', HTML1, re.M))) + 1

    for a in range(count):
        if a == 0:
            continue
        elif a == 1:
            htms_Value = re.findall(r'<mip-img,src="(.*?)">,', HTML, re.M)
        else:
            url = re.findall(r'^(.*?).html', item, re.M)[0]+"-"+str(a)+".html"
            r = requests.get(url)
            r.encoding = "utf-8"
            HTML = r.text
            HTML = HTML.split()
            HTML = ','.join(HTML)
            HTML1 = HTML
            htms_Value = re.findall(r'<mip-img,src="(.*?)">,', HTML, re.M)
        print("正在扒取第"+str(a)+"页...")
        r = requests.get(htms_Value[0])
        f = open("./%s" % a + ".jpg", "wb")
        f.write(r.content)
        f.close()
        r.close()
    time.sleep(120)
    i+=1

print("结束")