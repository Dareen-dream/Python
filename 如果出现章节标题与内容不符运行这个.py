import requests
import os
import re

 # 1. 修改因为跳章问题而造成的文件夹命名错误

url = "https://m.36mh.com/manhua/tongjunanguimi/"
head = { "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Mobile Safari/537.36" }
path = '/同居男闺蜜/'

r = requests.get(url,headers=head)
r.encoding = "utf-8"
HTML = ','.join(r.text.split())

for e in ["\\n", "\\t", "\\r", "\\", ":", "*", "\"", "|", "?"]:
    HTML = HTML.replace(e, "")

htms_key = re.findall(r"<span>(.*?)</span>",','.join(re.findall(r"<span>.*?</span>", HTML,re.M)) ,re.M)

# 从第几章开始修改文件夹名字
a = 101
os.chdir(path)

# 错误的文件夹列表
error_file_list = os.listdir(os.getcwd())

# 正确的文件夹列表
for i in range(len(htms_key)):
    htms_key[i] = str(i) + htms_key[i]
print(htms_key)
# 排序后的错误的文件夹列表
for i in range(len(error_file_list)):
    for j in range(0,len(error_file_list)-i-1):
        if eval(re.findall(r'\d+',error_file_list[j])[0]) > eval(re.findall(r'\d+',error_file_list[j+1])[0]):
            error_file_list[j],error_file_list[j+1] = error_file_list[j+1],error_file_list[j]

for y in range(len(htms_key)):
    if y < a :
        continue

    os.renames(error_file_list[y],htms_key[y])

print("文件夹重命名成功")
