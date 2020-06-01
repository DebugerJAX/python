import requests
import re
import xlwt,xlrd
import os

def get_num(url):
    wb=requests.get(url,headers=headers)
    wb.encoding=wb.apparent_encoding
    wbdata=wb.text.split('<')
    for i in range(len(wbdata)):
        if wbdata[i].startswith('em id='):
            aa=wbdata[i].split('>')
            num=aa[1]
            if '万' in num:
                num1=float(num.replace('万',''))*10000
            elif '亿' in num:
                num1=float(num.replace('亿',''))*100000000
            return(num1)
            # print(num)

def get_title(url):
    wb = requests.get(url, headers=headers)
    wb.encoding = wb.apparent_encoding
    wbdata = wb.text
    title_str = re.findall('name="title" content=.*', wbdata)
    if title_str:
        title=title_str[0].split(' ')
        title1=title[1].replace('content="','')
        # print(title[1])
        return(title1)

if __name__ == "__main__":
    cookie='pgv_pvi=9294307328; ptui_loginuin=598564346; RK=LfjkfTO2Y9; ptcz=ff0c0ddbe7b003a1891204d1d575e3ad1627ce75bd6e4f87ef013448667a359a; pgv_pvid=9222305988; tvfe_boss_uuid=c7151d80a1172cf9; video_guid=66066166ce686bb7; video_platform=2; pgv_info=ssid=s5413384000'
    headers={
        'User_Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Cookie':cookie
    }
    url='https://v.qq.com/channel/net_tv'
    wb=requests.get(url,headers=headers)
    # print(wbdata)
    wb.encoding=wb.apparent_encoding
    wbdata=wb.text
    url_list=re.findall('https:.*html',wbdata)
    title_list=[]
    num_list=[]
    for i in range(len(url_list)):
        title=get_title(url_list[i])
        if title not in title_list:
            title_list.append(title)
            # print(title_list)
            num=get_num(url_list[i])
            num_list.append(num)
    os.chdir('C:/Users/Administrator/Desktop')
    wb=xlwt.Workbook()
    ws=wb.add_sheet('腾讯视频观看量')
    for i in range(len(num_list)):
        ws.write(i,1,num_list[i])
        ws.write(i,0,title_list[i])
        wb.save('test.xls')