from pyquery import PyQuery as pq
import re

def extract_one_pate_pi_info(pi_link):
    persoanl_page = pq(pi_link, encoding='utf-8')
    chinese_name = persoanl_page(
        'body > div > div.main > div > div.intro.mobile > div.basic_info > p:nth-child(1)').text()
    english_name = persoanl_page(
        'body > div > div.main > div > div.intro.mobile > div.basic_info > p:nth-child(2)').text()[:-7]
    school = persoanl_page('body > div > div.main > div > div.intro.mobile > div.basic_info > p.school')
    school = re.search('school1="(.*?)"', school.text()).group(1)
    website = persoanl_page(
        'body > div > div.main > div > div.intro.mobile > div.basic_info > div > p:nth-child(3) a').text()
    resume = persoanl_page('body > div > div.main > div > div.main_intro > div > div').text()
    return chinese_name, english_name, school, website, resume


from tqdm import tqdm

pi_dic = {}
file_list = ['result/xihu_pi_info_url_engineering.txt', 'result/xihu_pi_info_url_science.txt',
             'result/xihu_pi_info_url_SLS.txt', ]
for pi_file in file_list:
    print(pi_file)
    with open(pi_file) as f:
        links = f.readlines()
        for pi_link in tqdm(links):
            print(pi_link)
            chinese_name, english_name, school, website, resume = extract_one_pate_pi_info(pi_link)
            pi_dic[chinese_name] = [english_name, school, website, resume]
