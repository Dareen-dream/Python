import requests
import os
import re
import time
import socket

#  1. 当被服务器识别为爬虫中断链接后可以自动重新继续爬取
#  2. 写入文件后的关闭（f.close）如果在try里面会被识别为错误
#  3. 加入延迟参数，当网页在预估时间内没有返回信息，重新爬取
#  4. 修改因为某些章节因为不符合正则表达式的原因而造成的跳章爬取

def 同居男闺蜜(End_Chapyer,End_Page):
    url = "https://m.36mh.com/manhua/tongjunanguimi/"
    head = { "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Mobile Safari/537.36" }
    path = '/1同居男闺蜜/'

    # 超时参数
    socket.setdefaulttimeout(20)

    # 获取网页源代码
    r = requests.get(url,headers=head)
    r.encoding = "utf-8"
    HTML = ','.join(r.text.split())

    htms_Value = re.findall(r"http://m.36mh.com/manhua/tongjunanguimi/\d{6}.html", HTML,re.M)
    htms_key = re.findall(r"<span>(.*?)</span>",','.join(re.findall(r"<span>.*?</span>", HTML,re.M)) ,re.M)

    # 第几话的第几页开始爬取
    # 上次截止为：19 12
    # End_Chapter = eval(input("请输入你要从第几章开始爬取："))
    # End_Page = eval(input("请输入你要从第"+str(End_Chapter)+"章的第几页开始开始爬取："))

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
            try:
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
                    # 易出错地
                    r = requests.get(url,headers=head,timeout=30)

                    r.encoding = "utf-8"
                    HTML = ','.join(r.text.split())
                    HTML1 = HTML
                    htms_Value = re.findall(r'<mip-img,src="(.*?)">,', HTML, re.M)
                print("正在扒取第"+str(Start_Page)+"页...")
                # time.sleep(1)

                r = requests.get(htms_Value[0],headers=head)
                f = open("./%s" % Start_Page + ".jpg", "wb")
                f.write(r.content)

            except Exception as e:
                print("出现错误，10秒钟后自动重新开始爬取")
                time.sleep(10)
                return Start_Chapter,Start_Page
            f.close()

        if count>50:
            print("30秒后自动开始爬取下一话")
            time.sleep(30)

    print("结束")
    Start_Chapter=-1
    Start_Page=-1
    return Start_Chapter,Start_Page

End_Chapter = eval(input("请输入你要从第几章开始爬取："))
End_Page = eval(input("请输入你要从第"+str(End_Chapter)+"章的第几页开始开始爬取："))

while True:
    End_Chapter,End_Page = 同居男闺蜜(End_Chapter,End_Page)
    if End_Chapter == -1:
        if End_Page == -1:
            print("爬起完毕！")
            exit(0)
    else:
        print("正在重新爬取")