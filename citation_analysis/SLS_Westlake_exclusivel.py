import json
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
import warnings
warnings.filterwarnings("ignore")
all_school_path=Path(r'F:\0_Desktop\Citation_Analysis\result\Westlake_pi_google_scholar_info.json')
SLS_path=Path(r'F:\0_Desktop\Citation_Analysis\result\Westlake_School_of_life_science_scholar_info.json')
all_school=json.load(all_school_path.open())
westlake_pi_csv_table = pd.read_csv('result/westlake_pi_csv_table.csv')
#%%
nan_mask = westlake_pi_csv_table['english_name'].isna()
westlake_pi_csv_table.english_name=westlake_pi_csv_table['english_name'].str.split(',').str[0]
westlake_pi_csv_table['english_name'][nan_mask]=westlake_pi_csv_table['Chinese name'].str.split(',').str[0]

#%%
name_list=westlake_pi_csv_table[
    westlake_pi_csv_table.school.str.contains('生命')
].english_name.to_list()
#%%
# westlake_pi_csv_table.to_csv('result/westlake_pi_csv_table.csv',index=False,)
#%%


#%%
sls_info={name: all_school[name] for name in name_list}
json.dump(sls_info,SLS_path.open('w'))
