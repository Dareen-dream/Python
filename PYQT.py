import requests
import os
import re
import time
import socket
import PyQt5

#  1. 添加自动保存上次的爬取位置，并在下次爬取的时候继续
#  2. 可以选择是继续上次的爬取还是自定义爬取的章节

def 同居男闺蜜(End_Chapyer, End_Page):
    url = "https://m.36mh.com/manhua/tongjunanguimi/"
    head = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Mobile Safari/537.36"}
    path = '/同居男闺蜜/'

    # 超时参数
    socket.setdefaulttimeout(20)

    # 获取网页源代码
    r = requests.get(url, headers=head)
    r.encoding = "utf-8"
    HTML = ','.join(r.text.split())

    htms_Value = re.findall(r"http://m.36mh.com/manhua/tongjunanguimi/\d{6}.html", HTML, re.M)
    htms_key = re.findall(r"<span>(.*?)</span>", ','.join(re.findall(r"<span>.*?</span>", HTML, re.M)), re.M)

    # 第几话的第几页开始爬取
    # 上次截止为：19 12
    # End_Chapter = eval(input("请输入你要从第几章开始爬取："))
    # End_Page = eval(input("请输入你要从第"+str(End_Chapter)+"章的第几页开始开始爬取："))

    for item, Start_Chapter in zip(htms_Value, range(len(htms_Value))):

        if End_Chapter > Start_Chapter:
            continue
        print("》》》准备扒取：" + str(Start_Chapter) + htms_key[Start_Chapter])

        # 删除特殊字符
        for e in ["\\n", "\\t", "\\r", "/", "\\", ":", "*", "\"", "<", ">", "|", "?"]:
            htms_key[Start_Chapter] = htms_key[Start_Chapter].replace(e, "")

        if (os.path.exists(path + str(Start_Chapter) + htms_key[Start_Chapter])):
            flag = 1
        else:
            os.makedirs(path + str(Start_Chapter) + htms_key[Start_Chapter])
            flag = 0
        os.chdir(path + str(Start_Chapter) + htms_key[Start_Chapter])

        r = requests.get(item, headers=head)
        r.encoding = "utf-8"
        HTML = ','.join(r.text.split())
        HTML1 = HTML
        count = eval(''.join(re.findall(r'<span,id="k_total",class="curPage">(.*?)</span>', HTML1, re.M)))
        print("本话共有：" + str(count) + "张漫画")

        for Start_Page in range(count + 1):
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
                    url = re.findall(r'^(.*?).html', item, re.M)[0] + "-" + str(Start_Page) + ".html"
                    # 易出错地
                    r = requests.get(url, headers=head, timeout=30)

                    r.encoding = "utf-8"
                    HTML = ','.join(r.text.split())
                    HTML1 = HTML
                    htms_Value = re.findall(r'<mip-img,src="(.*?)">,', HTML, re.M)
                print("正在扒取第" + str(Start_Page) + "页...")
                # time.sleep(1)

                r = requests.get(htms_Value[0], headers=head)
                f = open("./%s" % Start_Page + ".jpg", "wb")
                f.write(r.content)

            except Exception as e:
                print("出现错误，10秒钟后自动重新开始爬取")
                time.sleep(10)
                return Start_Chapter, Start_Page
            f.close()

        if count > 50:
            print("30秒后自动开始爬取下一话")
            time.sleep(30)

    print("结束")

    f = open(path+"上次爬取截止的位置.txt", "w")
    End_seat = str(Start_Chapter) + '\n' + str(Start_Page)
    f.write(End_seat)
    f.close()

    Start_Chapter = -1
    Start_Page = -1
    return Start_Chapter, Start_Page

# def printentry():
#     a = var.get()
#
# window = tkinter.Tk()
# var = tkinter.StringVar()
# window.title("同居男闺蜜")
# window.geometry("500x300")
# End_Chapter_1 = tkinter.Label(window, text="请输入你要从第几章开始爬取：", bg="blue", font=("Arial", 12), width=30, height=2)
# End_Chapter_1.pack()
# End_Chapter_2 = tkinter.Entry(window, show=None, font=("Arial", 14))
# End_Chapter_2.pack()
# End_Chapter =tkinter.Button(window,text="print entry",command=printentry).pack()
# End_Page_1 = tkinter.Label(window, text="请输入你要从第几章开始爬取：", bg="blue", font=("Arial", 12), width=30, height=2)
# End_Page_1.pack()
# End_Page_2 = tkinter.Entry(window, show=None, font=("Arial", 14))
# End_Page_2.pack()
# End_Page =tkinter.Button(window,text="print entry",command=printentry).pack()
# print(End_Chapter)
# print(type(End_Chapter))
# window.mainloop()

End_Chapter = eval(input("请输入你要从第几章开始爬取："))
End_Page = eval(input("请输入你要从第" + str(End_Chapter) + "章的第几页开始开始爬取："))

while True:
    End_Chapter, End_Page = 同居男闺蜜(End_Chapter, End_Page)
    if End_Chapter == -1:
        if End_Page == -1:
            print("爬起完毕！")
            exit(0)
    else:
        print("正在重新爬取")