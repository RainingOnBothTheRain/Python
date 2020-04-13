#2020.04.06  着手学习网络爬虫 参考B站收藏


import requests   #需要使用pip安装该库
import re         #正则表达式  用以匹配网站
import time       #延时
import os         #判断系统文件夹下是否存在某文件夹

#请求网页

#直接用网页上的uagent即可反爬
headers={
  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
    }

#该网站具有反爬功能，得手动添加头，不让其知道是爬虫.若不具备反爬，则不需要添加headers
response=requests.get('https://www.vmgirls.com/13679.html',headers=headers)
print(response.request.headers)
#print(response.text)
html=response.text


#解析网页,在html中进行匹配。此处在需要爬取的网页中右键检查，即可查看到命名及匹配图片数据的代码，编写规则即可

#保存进文件夹中,利用网站上给的图片标题命名
dir_name=re.findall('<h1 class="post-title h3">(.*?)</h1>',html)[-1]
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

#使用正则表达式  匹配具备该规则的图片 
urls = re.findall('<a href="(.*?)" alt=".*?" title=".*?">',html)
#print(urls)


#保存图片,先请求图片
for url in urls:
    time.sleep(1)
    #图片名字 取网站图片的名字，表示取倒数第一个命名
    filename=url.split('/')[-1]
    response=requests.get(url,headers=headers)
    with open (dir_name+'/'+filename,'wb') as f:
        f.write(response.content)   #写入图片
