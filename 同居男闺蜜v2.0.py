import requests
import os
import re
import time
import socket

#  1. 加了一个请求头
#  2. 加了一些人性化的提示

url = "https://m.36mh.com/manhua/tongjunanguimi/"
head = { "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Mobile Safari/537.36" }
path = '/同居男闺蜜/'

socket.setdefaulttimeout(20)

r = requests.get(url,headers=head)
r.encoding = "utf-8"
HTML = r.text
HTML = HTML.split()
HTML = ','.join(HTML)

htms_Value = re.findall(r"http://m.36mh.com/manhua/tongjunanguimi/\d{6}.html", HTML,re.M)
htms_key = re.findall(r"<span>(.*?)</span>",','.join(re.findall(r"<span>第.*?</span>", HTML,re.M)) ,re.M)

# 第几话的第几页开始爬取

i = 41
b = 0
c = 0
d = 0

for item in htms_Value:

    if c < i:
        c += 1
        continue

    print("》》》准备扒取：" + str(i) + htms_key[i])
    if (os.path.exists(path + str(i) + htms_key[i].strip().replace('\\n','').replace("\\t","").replace("\\r","").replace("/","").replace("\\","").replace(":","").replace("*","").replace("\"","").replace("<","").replace(">","").replace("|","").replace("?",""))):
        flag = 1
    else:
        os.makedirs(path + str(i) + htms_key[i].strip().replace('\\n','').replace("\\t","").replace("\\r","").replace("/","").replace("\\","").replace(":","").replace("*","").replace("\"","").replace("<","").replace(">","").replace("|","").replace("?",""))
        flag = 0
    os.chdir(path + str(i) + htms_key[i].strip().replace('\\n','').replace("\\t","").replace("\\r","").replace("/","").replace("\\","").replace(":","").replace("*","").replace("\"","").replace("<","").replace(">","").replace("|","").replace("?",""))
    r = requests.get(item,headers=head)
    r.encoding = "utf-8"
    HTML = r.text
    HTML = HTML.split()
    HTML = ','.join(HTML)
    HTML1 = HTML
    count = eval(''.join(re.findall(r'<span,id="k_total",class="curPage">(.*?)</span>', HTML1, re.M))) + 1
    print("本话共有："+str(count-1)+"张漫画")

    for a in range(count):

        if d<b:
            d += 1
            continue

        if a == 0:
            continue
        elif a == 1:
            htms_Value = re.findall(r'<mip-img,src="(.*?)">,', HTML, re.M)
        else:
            url = re.findall(r'^(.*?).html', item, re.M)[0]+"-"+str(a)+".html"
            r = requests.get(url,headers=head)
            r.encoding = "utf-8"
            HTML = r.text
            HTML = HTML.split()
            HTML = ','.join(HTML)
            HTML1 = HTML
            htms_Value = re.findall(r'<mip-img,src="(.*?)">,', HTML, re.M)
        print("正在扒取第"+str(a)+"页...")
        time.sleep(1)
        r = requests.get(htms_Value[0],headers=head)
        f = open("./%s" % a + ".jpg", "wb")
        f.write(r.content)
        f.close()
        r.close()

    if count>50:
        print("30秒后自动开始爬取下一话")
        time.sleep(30)

    i+=1

print("结束")