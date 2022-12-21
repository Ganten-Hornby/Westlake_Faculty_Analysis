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
    'Caltech': Path(r'F:\0_Desktop\Citation_Analysis\result\caltech\caltech_pi_google_scholar_info.json'),
    'JHU':Path(r'F:\0_Desktop\Citation_Analysis\result\JHU\JHU_pi_google_scholar_info.json'),
    'MIT':Path(r'F:\0_Desktop\Citation_Analysis\result\mit\mit_pi_google_scholar_info.json'),
    'Princeton':Path(r'F:\0_Desktop\Citation_Analysis\result\princeton\princeton_faculty_google_scholar_info.json'),
    'Stanford':Path(r'F:\0_Desktop\Citation_Analysis\result\stanford\stanford_pi_google_scholar_info.json'),
    'Westlake':Path(r'F:\0_Desktop\Citation_Analysis\result\Westlake_School_of_life_science_scholar_info.json'),
    # 'Westlake':Path(r'F:\0_Desktop\Citation_Analysis\result\Westlake_pi_google_scholar_info.json'),
    'THU':Path(r'F:\0_Desktop\Citation_Analysis\result\THU\thu_pi_google_scholar_info.json'),
    'PKU':Path(r'F:\0_Desktop\Citation_Analysis\result\PKU\pku_pi_google_scholar_info.json'),
    'SUSTech':Path(r'F:\0_Desktop\Citation_Analysis\result\sustech\sustech_pi_google_scholar_info.json'),
    'Harvad':Path(r'F:\0_Desktop\Citation_Analysis\result\harvard\harvard_pi_google_scholar_info.json'),
}
#%%
# data format transform
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

#%%
cite_per_year_records_label=['school_name','faculty_name','year','cite']
cite_per_year_records=[]
faculty_meta_info_records_label=['school_name','faculty_name','affiliation','citedby5y','hindex','hindex5y','i10index','i10index5y']
faculty_meta_info_records=[]
faculty_publication_records=[]
faculty_publication_records_labels=['school_name','faculty_name','index','publication_year','num_citations','title','source']
for school_name,school_dic in school_total_notnan.items():
    for people_name,container in school_dic.items():
        faculty_meta_info_records.append([school_name,people_name,container['affiliation'],container['citedby5y'],container['hindex'],container['hindex5y'],container['i10index'],container['i10index5y']])
        for year,year_cite in container['cites_per_year'].items():
            cite_per_year_records.append([school_name,people_name,year,year_cite])
        for i,pub_container in enumerate(container['publications'],1):
            faculty_publication_records.append([school_name,people_name,i,pub_container['bib'].get('pub_year',''),pub_container['num_citations'],pub_container['bib']['title'],pub_container['bib']['citation']])


cite_per_year_df=pd.DataFrame.from_records(cite_per_year_records,columns=cite_per_year_records_label)
faculty_meta_info_df=pd.DataFrame.from_records(faculty_meta_info_records,columns=faculty_meta_info_records_label)
faculty_publication_df=pd.DataFrame.from_records(faculty_publication_records,columns=faculty_publication_records_labels)
Result_ROOT=Path(r'F:\0_Desktop\Citation_Analysis\result\total')

cite_per_year_df.to_csv(Result_ROOT/'cite_per_year_df.csv',)
faculty_meta_info_df.to_csv(Result_ROOT/'faculty_meta_info_df.csv',)
faculty_publication_df.to_csv(Result_ROOT/'faculty_publication_df.csv',)
