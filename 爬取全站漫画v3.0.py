import requests
import os
import re
import time
import socket
import tkinter
import tkinter.messagebox

 # 1. 从只能爬取同居男闺蜜这个漫画到可以爬取36漫画的全部漫画
 # 2. 增加了漫画的搜索功能
 # 3. 弹窗的返回值不会使用
 # 4. 增加展示漫画的弹窗

def 搜索36漫画_Name():
    Date = ""

    def print_Name():
        global Date
        Date = Date_2.get()

    window = tkinter.Tk()
    window.title("搜索漫画")
    window.geometry("500x300")
    Date_1 = tkinter.Label(window, text="请输入你要搜索的漫画名或者作者名：", bg="skyblue", font=("Arial", 12), width=30, height=2)
    Date_1.pack()
    Date_2 = tkinter.Entry(window, show=None, font=("Arial", 14))
    Date_2.pack()
    tkinter.Button(window,text="print entry",command=print_Name).pack()
    window.mainloop()


def 展示漫画(htms_key):
    window = tkinter.Tk()
    window.title("选择漫画")
    window.geometry("500x300")
    var1 = tkinter.StringVar()  # 定义一个变量用来接收
    tkinter.Label(window, bg='yellow', textvariable=var1, width=15).pack()
    thelb = tkinter.Listbox(window)
    thelb.pack()
    for i in htms_key:
        thelb.insert(tkinter.END, i)

    def show():
        value = thelb.get(thelb.curselection())  # 获取光标在这个listbox上选定的值
        var1.set(value)
        print(value)
        for i, o in zip(htms_key, range(len(htms_key))):
            if i == value:
                global Name_value
                Name_value = o

    tkinter.Button(window, text='获取', command=show).pack()
    tkinter.mainloop()


def 搜索36漫画():
    搜索36漫画_Name()
    urls = "https://m.36mh.com/search/?keywords="
    head = { "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Mobile Safari/537.36"}
    url = urls + Date

    # 获取网页源代码
    r = requests.get(url, headers=head)
    r.encoding = "utf-8"
    HTML = ','.join(r.text.split())
    htms_Value = re.findall(r'class="title",href="(https://m.36mh.com/manhua/.*?/)",', HTML, re.M)
    htms_key = re.findall(r'class="title",href="https://m.36mh.com/manhua/.*?/",target="_blank">(.*?)</a>', HTML, re.M)
    展示漫画(htms_key)
    print(Name_value)
    print(type(Name_value))
    return htms_Value[Name_value], htms_key[Name_value]


def 爬取全站漫画(End_Chapter, End_Page, url, title):
    # url = "https://m.36mh.com/manhua/tongjunanguimi/"
    head = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/76.0.3809.100 Mobile Safari/537.36"}
    path = '/'+ title + '/'
    # 超时参数
    socket.setdefaulttimeout(20)
    # print(url)
    # 获取网页源代码
    r = requests.get(url, headers=head)
    r.encoding = "utf-8"
    HTML = ','.join(r.text.split())


    # 问题：正则表达式里面添加变量
    # 直接匹配，无法匹配，只能先匹配然后再拼接，但是这样匹配的有问题
    htms_Value = re.findall(r"\d{6}.html", HTML, re.M)
    # print(htms_Value)
    for i,x in zip(htms_Value,range(len(htms_Value))):
        htms_Value[x] = str(url) + str(htms_Value[x])
    # htms_Value = re.findall(r"('+url+')\d{6}.html", HTML, re.M)
    # htms_Value = re.findall(r"(%s)\d{6}.html"%url, HTML, re.M)
    # re.finditer(r'(%s)(\d{1,3})(\s*</td>\s+<td>\d{1,3}</td>\s*)(<td>)(\d{1,3})(\s*</td>)'% (path, u'[\u4e00-\u9fa5]'
    # ), url)  # 卧槽，这种问题解决了不容易啊，纪念一下！！！

    htms_key = re.findall(r"<span>(.*?)</span>", ','.join(re.findall(r"<span>.*?</span>", HTML, re.M)), re.M)

    # 解决上面问题后可以只有下面的代码
    # for item, Start_Chapter in zip(htms_Value, range(len(htms_Value))):
    for item, Start_Chapter in zip(htms_Value, range(len(htms_key))):

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

    # 出现bug，在此处无法运行
    # f = open(path+"上次爬取截止的位置.txt", "w")
    # End_seat = str(Start_Chapter) + '\n' + str(Start_Page)
    # f.write(End_seat)
    # f.close()

    Start_Chapter = -1
    Start_Page = -1
    return Start_Chapter, Start_Page


def windows(titles):
    End_Chapter, End_Page = 0, 0
    def print_End_Chapter():
        global End_Chapter
        End_Chapter = End_Chapter_2.get()
        tkinter.messagebox.showinfo(title=titles, message="你即将要从第"+str(End_Chapter)+"章开始爬取")

    def print_End_Page():
        global End_Page
        End_Page = End_Page_2.get()
        tkinter.messagebox.showinfo(title=titles, message="你即将要从第" + str(End_Chapter) + "章"+ str(End_Page) +"页开始爬取")

    window = tkinter.Tk()
    window.title(titles)
    window.geometry("500x300")
    End_Chapter_1 = tkinter.Label(window, text="请输入你要从第几章开始爬取：", bg="skyblue", font=("Arial", 12), width=30, height=2)
    End_Chapter_1.pack()
    End_Chapter_2 = tkinter.Entry(window, show=None, font=("Arial", 14))
    End_Chapter_2.pack()
    tkinter.Button(window,text="print entry",command=print_End_Chapter).pack()

    # 窗口无法实时更新数据
    # End_Page_1 = tkinter.Label(window, text="请输入你要从第"+str(End_Chapter)+"章的第多少页开始爬取：", bg="skyblue", font=("Arial", 12), width=30, height=2)
    End_Page_1 = tkinter.Label(window, text="请输入你要从第多少页开始爬取：", bg="skyblue", font=("Arial", 12),width=30, height=2)
    End_Page_1.pack()
    End_Page_2 = tkinter.Entry(window, show=None, font=("Arial", 14))
    End_Page_2.pack()
    tkinter.Button(window,text="print entry",command=print_End_Page).pack()

    window.mainloop()

if __name__ == '__main__':
    url_, title = 搜索36漫画()
    windows(title)
    End_Chapter,End_Page=eval(End_Chapter)-1,eval(End_Page)
    while True:
        End_Chapter, End_Page = 爬取全站漫画(End_Chapter, End_Page, url_, title)
        if End_Chapter == -1:
            if End_Page == -1:
                print("爬起完毕！")
                exit(0)
        else:
            print("正在重新爬取")
