import os
import requests
from bs4 import BeautifulSoup

# parameter
article = ''

header = {'accept': 'application/json, text/plain, */*',
          'accept-encoding': 'gzip, deflate, br',
          'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
          'origin': 'https://mp.weixin.qq.com',
          'sec-fetch-dest':'empty',
          'sec-fetch-mode':'cors',
          'sec-fetch-site':'same-origin',
          'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) \
                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 \
                        Safari/537.36'
         }
img_header = {
    'accept': 'text/html,application/xhtml+xml,\
              application/xml;q=0.9,image/avif,image/webp,image/apng,\
              */*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cache-control': 'max-age=0',
    'sec-fetch-dest':'document',
    'sec-fetch-mode':'navigate',
    'sec-fetch-site':'cross-site',
    'sec-fetch-user':'?1',
    'upgrade-insecure-requests':'1',
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 \
                Safari/537.36'
}

def fetchArticle(article):
    print('[Info] Fetching content ...')
    url = 'https://mp.weixin.qq.com/s/'+article
    website = requests.get(url, headers=header)
    soup = BeautifulSoup(website.text, 'lxml')
    output_html = soup.prettify()
    imgs = soup.findAll('img')
    img_urls = []
    for imgs in imgs:
        try:
            img_urls.append(imgs['data-src'])
        except:
            print('Blank image')

    if not os.path.isdir(article):
        os.mkdir(article)
    img_dict = {}

    print('[Info] Fetching images...')
    for i, img_url in enumerate(img_urls):
        try:
            img_format = img_url.split('=')[-1]
            img_response = requests.get(img_url,headers=img_header)
            file = open("{}/{}.{}".format(article,i,img_format), "wb")
            img_dict[img_url] = "{}/{}.{}".format(article,i,img_format)
            file.write(img_response.content)
            file.close()

            old_img = 'data-src="'+img_url+'"'
            new_img = 'src="'+img_dict[img_url]+'"'
            output_html = output_html.replace(old_img,new_img)
        except:
            print('error')
    return output_html

def outputWeb(output_html):
    # replace width
    for i in range(20,80,5):
        ori_width = i
        new_width = i-1
        output_html = output_html.replace('width: '+str(ori_width)+'%','width: '+str(new_width)+'%')
    print('[Info] Output file...')
    f = open(article+".html", "w")
    f.write(output_html)
    f.close()
    print('[Info] Done')

output_html = fetchArticle(article)
outputWeb(output_html)