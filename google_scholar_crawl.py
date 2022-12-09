# %%
import json
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from tqdm import tqdm

from scholarly import scholarly,ProxyGenerator
import requests
import logging
from selenium import webdriver
import logging
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
# chrome_options.headless = True
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome_options)
scholarly.set_driver(driver)

#%%
def search_author(name, email_domain='westlake', affiliation='westlake',):
    print(f'=======start searching {name}======')
    search_query = scholarly.search_author(name)
    for i, author in enumerate(search_query):
        print(i)
        if (affiliation in author['affiliation'].lower()) or (email_domain in author['email_domain'].lower()):
            print(f'!!!! find {name}')
            return scholarly.fill(author)
        if i >= 10:
            search_query = scholarly.search_author(name + f' {affiliation}')
            for author in search_query:
                if (affiliation in author['affiliation'].lower()) or (email_domain in author['email_domain'].lower()):
                    print(f'!!!! find {name} by adding {affiliation} suffix******************')
                    return scholarly.fill(author)
            break
    print(f'-------------Not find {name}')
    return None
def fill_author_container_publication(author_container):
    if author_container is not None:
        for pub in tqdm(author_container['publications'][:100]):
            try:
                pub.update(scholarly.fill(pub,))
                # print(pub['bib']['title'],'Successful')
            except:
                pass



# author = search_author('jian ')

def crawl_author_list_by(name_list,fill_publication=False,email_domain='westlake', affiliation='westlake',enhance_search=False):
    begin = time.time()
    info_dict={}
    i=0
    for name in tqdm(name_list):
        author_container=search_author(name,email_domain,affiliation)
        if author_container is None:
            if enhance_search:
                author_container=enhance_search_author(name,email_domain,affiliation)
        if author_container is not None:
            i+=1
            if fill_publication:
                fill_author_container_publication(author_container)
        info_dict[name]=author_container


    print(f'{time.time() - begin:.2f}s')
    print(f'among {len(name_list)}, {i/len(name_list):.2%} has google scholar page')
    return info_dict


def enhance_search_author(name, domain, affiliation):
    name_parts = name.split()
    first_name = name_parts[0]
    if len(name_parts) >2:
        last_name = name_parts[-1]
        author_container = search_author(first_name + ' ' + last_name, domain, affiliation)
        if author_container is not None:
            logging.critical(f'Enhancing searched {first_name +" " + last_name}')
            return author_container
        else:
            return None
    # author_container=search_author(first_name, domain, affiliation)
    # logging.critical(f'Enhancing searched {first_name}')
    # return author_container


def crawl_author_list_by_multi_thread(name_list, max_workers=40, ):
    begin = time.time()
    executor = ThreadPoolExecutor(max_workers=max_workers)
    for author_info, author_name in tqdm(zip(executor.map(search_author, name_list), name_list)):
        if author_info is not None:
            info_dict[author_name] = author_info
        else:
            info_dict[author_name] = 'NotFound in google scholar'
    times = time.time() - begin
    print(times, 's')
    return info_dict
    # #
    # with ThreadPoolExecutor(max_workers=20) as t:
    #     info_dict = {}
    #     obj_list = []
    #     for author_name in tqdm(name_list):
    #         obj = t.submit(search_author,author_name)
    #         obj_list.append(obj)
    #
    #     for future in as_completed(obj_list):
    #         author_info = future.result()
    #         if author_info is not None:
    #             info_dict[author_name] = author_info
    #         else:
    #             info_dict[author_name] = 'NotFound in google scholar'


# %%
if __name__ == '__main__':
    # %%
    westlake_pi_csv_table = pd.read_csv('result/westlake_pi_csv_table.csv')
    name_list = ['Simon Groeblacher',
                 'Alexey KAVOKIN',
                 'Pavlos SAVVIDIS',
                 'Kiryl D. Piatkevich']
    nan_mask = westlake_pi_csv_table['english_name'].isna()
    name_list += westlake_pi_csv_table.loc[~nan_mask]['english_name'].str.split(',').str[0].to_list()
    name_list = list(set(name_list))
    info_dict = crawl_author_list_by_multi_thread(name_list)
    with open('result/Westlake_pi_google_scholar_info.json', 'w') as f:
        json.dump(info_dict, f)

    # %%
    i = 0
    for author, info in info_dict.items():
        if info == 'NotFound in google scholar':
            i += 1
    print(i / len(info_dict))
