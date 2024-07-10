import requests
from bs4 import BeautifulSoup
import re
import csv
import sys

'''
使用 csv.writer
csv.writer 返回一个写入器对象，允许逐行写入数据。writerow 方法用于写入一行数据，writerows 方法用于写入多行数据。
'''
front_url='vessels?page='
base_url='https://www.vesselfinder.com/'
page=1

with open('test_for _vessel_finder.csv',mode='a',newline='') as vfinder:
    writer=csv.writer(vfinder)
    writer.writerow(['IMO number','Vessel Name','Ship type','Flag','Gross Tonnage','Summer Deadweight (t)','Length Overall (m)','Beam (m)'])

cookies = {
    'ROUTEID': '.1',
    '_ga': 'GA1.1.866887217.1720492499',
    'usprivacy': '1N--',
    '_pbjs_userid_consent_data': '6683316680106290',
    'cto_bundle': 'ioGBMF9oMzlnU2g4SXZDU0xPekloM0VZNGRNZEZvUktBTThYZGV5enlUR1RUNyUyQnBEZlZHallEUG5JMGdoYVJDRnpna3lCN2hBaCUyRk9MJTJGYnlzanJxVTd4RHBIJTJGQ3phaXZoMlQ2ZFpEaHFUT2dhM3NoVyUyQlJHR2x2RlVmSHclMkJVZExlSWZVbzdNWmdwT2R6c2V0a1E0WlV1d09FRnclM0QlM0Q',
    'cto_bidid': 'CZBKLF9NYVpiYzFZZ2w4emJkOWI1JTJCRVRWeUlUTm1FNldLd29kWnZYWDJ0czhRWktadUlGWjk3SnpiUnpKODh2cWRoSWdvJTJGWHZVOEMwOEF6SzhZNzJDY2ZRaXRkZnRkQlkyYng5dGZjYSUyRmJId2ZPWlZscDVJTXM4NEdoOXdHNFZlRmhleg',
    'cto_dna_bundle': 'TtsDkV9oMzlnU2g4SXZDU0xPekloM0VZNGRPdGtpSXpaczRGWHJNNUNFakg5ZmJwOXY2dVo5ViUyRlR0YlEyMjdVd0Q4R3RsTEZCSWZ3Y2hDQ1Q0RzhpSzlvVGJBJTNEJTNE',
    '_ga_0MB1EVE8B7': 'GS1.1.1720500094.2.0.1720500094.0.0.0',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # 'cookie': 'ROUTEID=.1; _ga=GA1.1.866887217.1720492499; usprivacy=1N--; _pbjs_userid_consent_data=6683316680106290; cto_bundle=ioGBMF9oMzlnU2g4SXZDU0xPekloM0VZNGRNZEZvUktBTThYZGV5enlUR1RUNyUyQnBEZlZHallEUG5JMGdoYVJDRnpna3lCN2hBaCUyRk9MJTJGYnlzanJxVTd4RHBIJTJGQ3phaXZoMlQ2ZFpEaHFUT2dhM3NoVyUyQlJHR2x2RlVmSHclMkJVZExlSWZVbzdNWmdwT2R6c2V0a1E0WlV1d09FRnclM0QlM0Q; cto_bidid=CZBKLF9NYVpiYzFZZ2w4emJkOWI1JTJCRVRWeUlUTm1FNldLd29kWnZYWDJ0czhRWktadUlGWjk3SnpiUnpKODh2cWRoSWdvJTJGWHZVOEMwOEF6SzhZNzJDY2ZRaXRkZnRkQlkyYng5dGZjYSUyRmJId2ZPWlZscDVJTXM4NEdoOXdHNFZlRmhleg; cto_dna_bundle=TtsDkV9oMzlnU2g4SXZDU0xPekloM0VZNGRPdGtpSXpaczRGWHJNNUNFakg5ZmJwOXY2dVo5ViUyRlR0YlEyMjdVd0Q4R3RsTEZCSWZ3Y2hDQ1Q0RzhpSzlvVGJBJTNEJTNE; _ga_0MB1EVE8B7=GS1.1.1720500094.2.0.1720500094.0.0.0',
    'priority': 'u=0, i',
    'referer': 'https://www.vesselfinder.com/vessels?page=2',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
}

def boat_info_analysis(url):
    response = requests.get(url, cookies=cookies, headers=headers)
    soup=BeautifulSoup(response.content,'html.parser')
    # title=soup.find('title')
    table=soup.find('table',class_='tparams')
    table_data=table.find_all('td',class_='v3')
    '''
    正则表达式：
    一个问题，为什么不能直接匹配table.text中的数据？有待调查
    '''
    #from title,get name and type:
    # title_date=re.match(r'(.+),\s(.+)\s-\sD',title.text)
    # but in this way,we need two find_all,one for title,one for the table,
    # i guess that would be slow,so we just fetch all data from data,that would be better.

    #used for debug:
    # print(table_date.group)
    # print(table_data[1].text)
    imo_num=table_data[0].text
    name=table_data[1].text
    type=table_data[2].text
    flag=table_data[3].text
    gross_Tonnage=table_data[5].text
    summer_Deadweight=table_data[6].text
    length=table_data[7].text
    beam=table_data[8].text
    this_ship=[imo_num,name,type,flag,gross_Tonnage,summer_Deadweight,length,beam]
    
    with open('test_for _vessel_finder.csv',mode='a',newline='') as vfinder:
        writer=csv.writer(vfinder)
        writer.writerow(this_ship)
    # print(this_ship)

'''
find_all 方法返回的是一个 ResultSet 对象。
ResultSet 是 BeautifulSoup 库中用于存储所有匹配结果的容器，它的行为类似于一个 Python 列表。
ResultSet 对象包含所有匹配的标签，每个标签都是一个 Tag 对象。

ResultSet 对象中的每个元素都是一个 Tag 对象。
Tag 对象表示一个 HTML 或 XML 标签，并且包含了该标签的属性、文本内容以及子标签。
'''
def front_page_analysis(page):
    previous_boat_info_url=base_url
    url=base_url+front_url+str(page)
    response = requests.get(url, cookies=cookies, headers=headers)
    if response.status_code!=200 :
        print("exit at page",page)
        sys.exit(0)#detect can fetch data from current page,end the program
    soup=BeautifulSoup(response.content,'html.parser')
    boats_info=soup.find_all('a',class_='ship-link')#all boats' link of current page
    for boat_info in boats_info:
        present_boat_info_url=base_url+boat_info['href']
        if previous_boat_info_url!=present_boat_info_url:
            boat_info_analysis(present_boat_info_url)#prevent useless repeat of same link of a boat from differnt_tag<a>
            previous_boat_info_url=present_boat_info_url
        
while True:
    front_page_analysis(page)
    page+=1