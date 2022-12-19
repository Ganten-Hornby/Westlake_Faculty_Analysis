import json
from pathlib import Path

import pandas as pd

from google_scholar_crawl import crawl_author_list_by

EMAIL_DOMAIN = AFFILIATION = 'stanford'

RESULT_PATH = Path.cwd().parents[1] / 'result/stanford'
RESULT_PATH.exists()
df = pd.read_csv(RESULT_PATH / 'standord_pi_name_url.csv', encoding='utf8')
name_list = df.name.to_list()
info_dic = crawl_author_list_by(name_list, email_domain=EMAIL_DOMAIN, affiliation=AFFILIATION, fill_publication=False,
                                enhance_search=True)
# %%
i = 0
for name in info_dic:
    if info_dic[name] is not None:
        i+=1
        # print('aaaa')
        # supp_info = crawl_author_list_by([name], email_domain=EMAIL_DOMAIN, affiliation=AFFILIATION,
        #                                  fill_publication=False,
        #                                  enhance_search=True)
        # if supp_info[name] is not None:
        #     info_dic[name]=supp_info[name]
        #     i+=1
print(i/len(info_dic))
# %%
with open(RESULT_PATH / 'stanford_pi_google_scholar_info.json', 'w') as f:
    json.dump(info_dic, f)
