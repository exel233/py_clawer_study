import requests
from bs4 import BeautifulSoup
import re
import csv
import json
import os
import time
import random

# 获取脚本文件的所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 将当前工作目录更改为脚本所在的目录
os.chdir(script_dir)

base_url='https://www.vesselfinder.com'
progress_filename = 'progress.json'

'''
使用 csv.writer
csv.writer 返回一个写入器对象，允许逐行写入数据。writerow 方法用于写入一行数据，writerows 方法用于写入多行数据。
'''
num_csv=1
scrapying_page_num=0
current_boat_index = 0

with open('test_for_vessel_finder'+str(num_csv)+'.csv', mode='a', newline='') as vfinder:
    writer = csv.writer(vfinder)
    writer.writerow(['IMO','MMSI', 'Callsign', 'Vessel Name', 'Ship type', 'Flag', 'Length Overall (m)', 'Beam (m)'])


# 定义保存和加载进度的函数
def save_progress(current_url, page, flag_index, type_value, num_csv, scrapying_page_num, current_boat_index, filename='progress.json'):
    progress_data = {
        'current_url': current_url,
        'page': page,
        'flag_index': flag_index,
        'type_value': type_value,
        'num_csv': num_csv,
        'scrapying_page_num': scrapying_page_num,
        'current_boat_index': current_boat_index
    }
    with open(filename, 'w') as f:
        json.dump(progress_data, f, indent=4)


def load_progress(filename='progress.json'):
    if os.path.exists(filename):
        # print(os.path.abspath(filename))
        with open(filename, 'r') as f:
            return json.load(f)
    return None

# 定义cookies和headers
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
    'accept': 'clean_clean_text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
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
    global page, flag_index, type_value,num_csv,scrapying_page_num,current_boat_index
    try:
        time.sleep(random.uniform(1, 3))  # 随机延迟
        response = requests.get(url, cookies=cookies, headers=headers)#cost 99% time in function
        if response.status_code != 200:
            print('this boat\'s info is 404')
            return None
        
        soup=BeautifulSoup(response.content,'html.parser')
        title=soup.find('title')
        first_table=soup.find('table',class_='aparams')#for IMO/MMSI,Callsign
        describe_text = soup.find('p', class_='text2')


        imo = mmsi = Callsign = flag = name = ship_type = length = beam = '-'


        if title:
            print(title.text)
            # from title,get name,type:
            title_date=re.match(r'(.+),\s(.+)\s-\sDetails\sand\scurrent\sposition\s-\s(.+)\s(.+)\s-\sV',title.text)
            # if title_date.group(3)=='IMO':
            #     imo=title_date.group(4)
            
                        
        #     if title_date.group(4)=='MMSI':
        #         mmsi=title_date.group(4)
        #         if first_table:
        #             first_table_data=first_table.find_all('td',class_='v3')
        #             # split_imo_mmsi=re.match(r'(.+)/(.+)',first_table_data[6].text)#make IMO and MMSI of the first table seperate
        #             if first_table_data[9].text!='-':
        #                 split_igth_beam=re.match(r'(.+)/(.+)m',first_table_data[9].text)#make length and beam of the first table seperate
        #                 length=split_igth_beam.group(1)
        #                 beam=split_igth_beam.group(2)

            name=title_date.group(1)
            ship_type=title_date.group(2)
        if describe_text:
            # Pattern to extract flag
            text = describe_text.get_text(strip=True)
            clean_text = ' '.join(text.split())  # 移除多余的空白字符
            # print(clean_text)
            # second_table=soup.find('table',class_='tparams')#for name and type
            flag_pattern = r"sailing under the flag of(.+)\."
            flag_match = re.search(flag_pattern, clean_text)
            if flag_match:
                flag = flag_match.group(1).strip()

            # Pattern to extract IMO
            imo_pattern = r"IMO (\d+)"
            imo_match = re.search(imo_pattern, clean_text)
            if imo_match:
                imo = imo_match.group(1).strip()

            # Pattern to extract MMSI
            mmsi_pattern = r"MMSI (\d+)"
            mmsi_match = re.search(mmsi_pattern, clean_text)
            if mmsi_match:
                mmsi = mmsi_match.group(1).strip()

            # Pattern to extract type
            type_pattern = r"is a ([A-Za-z\s]+) built"
            type_match = re.search(type_pattern, clean_text)
            if not type_match:  # Fallback for the other type of sentence structure
                type_pattern = r"is a ([A-Za-z\s]+) and currently"
                type_match = re.search(type_pattern, clean_text)
            if type_match:
                ship_type = type_match.group(1).strip()

        if first_table:
            first_table_data=first_table.find_all('td',class_='v3')
            # split_imo_mmsi=re.match(r'(.+)/(.+)',first_table_data[6].text)#make IMO and MMSI of the first table seperate
            # mmsi=split_imo_mmsi.group(2)
            if first_table_data[9].text!='-':
                split_igth_beam=re.match(r'(.+)/(.+)m',first_table_data[9].text)#make length and beam of the first table seperate
                length=split_igth_beam.group(1)
                beam=split_igth_beam.group(2)


            Callsign=first_table_data[7].text
            # flag=first_table_data[8].text

        # if second_table:
        #     second_table_data=second_table.find_all('td',class_='v3')
        #     name=second_table_data[1].text
        #     ship_type=second_table_data[2].text
        #     gross_Tonnage=second_table_data[5].text
        #     summer_Deadweight=second_table_data[6].text
        '''
        正则表达式：
        一个问题，为什么不能直接匹配table.text中的数据？有待调查
        '''
        #from title,get name and type:
        # title_date=re.match(r'(.+),\s(.+)\s-\sD',title.text)

        #used for debug:
        # print(table_data.group)
        # print(second_table_data[1].text)

        this_ship=[imo,mmsi,Callsign,name,ship_type,flag,length,beam]

        with open('test_for_vessel_finder'+str(num_csv)+'.csv',mode='a',newline='') as vfinder:
            writer=csv.writer(vfinder)
            writer.writerow(this_ship)
        print(this_ship)

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        save_progress(url, page, flag_index, type_value, num_csv, scrapying_page_num, current_boat_index, progress_filename)
        raise e


'''
find_all 方法返回的是一个 ResultSet 对象。
ResultSet 是 BeautifulSoup 库中用于存储所有匹配结果的容器，它的行为类似于一个 Python 列表。
ResultSet 对象包含所有匹配的标签，每个标签都是一个 Tag 对象。

ResultSet 对象中的每个元素都是一个 Tag 对象。
Tag 对象表示一个 HTML 或 XML 标签，并且包含了该标签的属性、文本内容以及子标签。
'''

def front_page_analysis(url):
    global page, flag_index, type_value, num_csv, scrapying_page_num, current_boat_index
    previous_boat_info_url = None
    print('current scraping url', url)
    try:
        time.sleep(random.uniform(1, 3))  # 随机延迟
        response = requests.get(url, cookies=cookies, headers=headers)  # cost 99% time before for
        if response.status_code != 200:
            print('no more page')
            return False

        soup = BeautifulSoup(response.content, 'html.parser')
        boats_info = soup.find_all('a', class_='ship-link')  # all boats' link of current page

        if not boats_info:  # Check if the list is empty
            print("No boats found on this page.")
            return False  # Indicate no boats found
        else:
            for i in range(current_boat_index, len(boats_info)):
                boat_info = boats_info[i]
                present_boat_info_url = base_url + boat_info['href']
                if previous_boat_info_url != present_boat_info_url:
                    print('now is', present_boat_info_url)
                    boat_info_analysis(present_boat_info_url)
                    previous_boat_info_url = present_boat_info_url
                current_boat_index = i + 1
            scrapying_page_num += 1  # record that already scraping 1 page
            current_boat_index = 0  # Reset current_boat_index after processing all boats in the current page
            return True  # Indicate boats found

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        save_progress(url, page, flag_index, type_value, num_csv, scrapying_page_num, current_boat_index, progress_filename)
        raise e



# 恢复爬取进度
progress_data = load_progress(progress_filename)
print(progress_data)
if progress_data:
    current_url = progress_data['current_url']
    page = progress_data['page']
    flag_index = progress_data['flag_index']
    type_value = progress_data['type_value']
    num_csv = progress_data['num_csv']
    scrapying_page_num = progress_data['scrapying_page_num']
    current_boat_index = progress_data['current_boat_index']
    print(f"Resuming from {current_url}",' and number',current_boat_index)
    print('continue write in csv', num_csv)
else:
    current_url = base_url + '/vessels'
    page = 1
    flag_index = 0
    type_value = 0
    num_csv = 1
    scrapying_page_num = 0
    current_boat_index = 0




initial_page = requests.get(current_url, cookies=cookies, headers=headers)
initial_page_soup = BeautifulSoup(initial_page.content, 'html.parser')
flag_select = initial_page_soup.find('select', id="advsearch-ship-flag")
all_flags = flag_select.find_all('option')

# 创建CSV文件并写入表头（如果文件不存在）

for flag_index in range(flag_index, len(all_flags)):
    flag = all_flags[flag_index]
    if flag['value'] != '-':
        flag_value = flag['value']
        for type_value in range(type_value, 9):
            while page <= 200:
                if scrapying_page_num>=500:
                    num_csv+=1
                    with open('test_for_vessel_finder'+str(num_csv)+'.csv', mode='a', newline='') as vfinder:
                        writer = csv.writer(vfinder)
                        writer.writerow(['IMO','MMSI', 'Callsign', 'Vessel Name', 'Ship type', 'Flag',  'Length Overall (m)', 'Beam (m)'])
                    scrapying_page_num=0
                url = f'{base_url}/vessels?page={page}&type={type_value}&flag={flag_value}'
                
                boats_found = front_page_analysis(url)
                if not boats_found:  # No boats found for this type and flag, skip to next type
                    break

                page += 1
            page = 1
        type_value = 0
