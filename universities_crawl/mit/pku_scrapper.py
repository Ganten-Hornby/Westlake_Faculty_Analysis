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
EMAIL_DOMAIN='pku'
AFFILIATION='peking'

RESULT_PATH = Path.cwd().parents[1] / 'result/PKU'
RESULT_PATH.exists()
thu_name_list=RESULT_PATH.joinpath('pku_faculty_name_pinyin_list.txt').read_text(encoding='utf8').split('\n')

info_dic=crawl_author_list_by(thu_name_list, email_domain=EMAIL_DOMAIN, affiliation=AFFILIATION, fill_publication=False,enhance_search=False)
#
#
with open(RESULT_PATH/'pku_pi_google_scholar_info.json', 'w') as f:
    json.dump(info_dic, f)
