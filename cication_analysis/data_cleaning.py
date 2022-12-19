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
#%%
json_file_path={
    'caltech': Path(r'F:\0_Desktop\Citation_Analysis\result\caltech\caltech_pi_google_scholar_info.json'),
    'JHU':Path(r'F:\0_Desktop\Citation_Analysis\result\JHU\JHU_pi_google_scholar_info.json'),
    'MIT':Path(r'F:\0_Desktop\Citation_Analysis\result\mit\mit_pi_google_scholar_info.json'),
    'princeton':Path(r'F:\0_Desktop\Citation_Analysis\result\princeton\princeton_faculty_google_scholar_info.json'),
    'stanford':Path(r'F:\0_Desktop\Citation_Analysis\result\stanford\stanford_pi_google_scholar_info.json'),
    'Westlake':Path(r'F:\0_Desktop\Citation_Analysis\result\Westlake_pi_google_scholar_info.json'),
}
#%%
# data format transform
df=json.load(Path(r'F:\0_Desktop\Citation_Analysis\result\caltech\caltech_pi_google_scholar_info.json').open())
#%%
school_total={}
school_total_path=Path(r'F:\0_Desktop\Citation_Analysis\result\total\school_total.json')
school_total_notnan={}
school_total_notnan_path=Path(r'F:\0_Desktop\Citation_Analysis\result\total\school_total_notnan.json')


for school_name,school_path in json_file_path.items():
    load = json.load(school_path.open())
    school_total[school_name]= load
    school_total_notnan[school_name]={k: v for k,v in load.items() if (v is not None)and (not isinstance(v,str))}
#%%
json.dump(school_total_notnan,school_total_notnan_path.open('w'),)
json.dump(school_total,school_total_path.open('w'),)







