import json
from pathlib import Path
import re
import os
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from pathlib import Path
from tqdm import tqdm, trange
from google_scholar_crawl import search_author, fill_author_container_publication,crawl_author_list_by
EMAIL_DOMAIN = AFFILIATION = 'caltech'

RESULT_PATH = Path.cwd().parents[1] / 'result/caltech'
RESULT_PATH.exists()
df=pd.read_csv(RESULT_PATH/'caltech_pi_name_url.csv', encoding='utf8')
name_list=df.name.to_list()
info_dic = crawl_author_list_by(name_list, email_domain=EMAIL_DOMAIN, affiliation=AFFILIATION, fill_publication=False,
                                enhance_search=True)


with open(RESULT_PATH/'caltech_pi_google_scholar_info.json', 'w') as f:
    json.dump(info_dic, f)


# len(a['publications'])
# len(b['publications'])
