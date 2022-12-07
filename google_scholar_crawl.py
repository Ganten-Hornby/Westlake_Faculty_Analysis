# %%
import json
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from scholarly import scholarly
from tqdm import tqdm
import requests

requests.get('https://scholar.google.com/',proxies={
   'http': 'http://127.0.0.1:7890',
   'https': 'https://127.0.0.1:7890',
})
requests.get('https://scholar.google.com/',)
# %%

author_name = 'Jian yang'
institution = 'westlake'

from scholarly import ProxyGenerator
pg = ProxyGenerator()
pg.FreeProxies()
scholarly.use_proxy(pg)
# Retrieve the author's data, fill-in, and print
# Get an iterator for the author results
# %%

def search_author(name=author_name, email_domain='westlake', affiliation='westlake'):
    print(f'=======start searching {name}======')
    search_query = scholarly.search_author(name)
    for i, author in enumerate(search_query):
        if (affiliation in author['affiliation'].lower()) or (email_domain in author['email_domain'].lower()):
            print(f'!!!! find {name}')
            return scholarly.fill(author)
        if i >= 10:
            search_query = scholarly.search_author(name + f' {affiliation}')
            for author in search_query:
                if ('westlake' in author['affiliation'].lower()) or ('westlake' in author['email_domain'].lower()):
                    print(f'!!!! find {name} by adding westlake suffix******************')
                    return scholarly.fill(author)
            break
    print(f'-------------Not find {name}')
    return None


author = search_author('jian ')


def crawl_filled_author(name_list, max_workers=40, ):
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
    info_dict = crawl_filled_author()
    with open('result/Westlake_pi_google_scholar_info.json', 'w') as f:
        json.dump(info_dict, f)

    # %%
    i = 0
    for author, info in info_dict.items():
        if info == 'NotFound in google scholar':
            i += 1
    print(i / len(info_dict))
