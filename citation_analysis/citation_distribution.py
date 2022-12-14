#%%

#%%
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
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)
school_total_path=Path(r'F:\0_Desktop\Citation_Analysis\result\total\school_total.json')
school_total=json.load(school_total_path.open())

#%%
import plotly.io as pio
pio.templates.default='plotly_white'
#%%
Result_ROOT=Path(r'F:\0_Desktop\Citation_Analysis\result\total')
cite_per_year_df=pd.read_csv(Result_ROOT/'cite_per_year_df.csv',index_col=0,)
faculty_meta_info_df=pd.read_csv(Result_ROOT/'faculty_meta_info_df.csv',index_col=0,)
faculty_publication_df=pd.read_csv(Result_ROOT/'faculty_publication_df.csv',index_col=0,)

#%%

df=cite_per_year_df.groupby(['school_name','year']).cite.mean().reset_index()
fig=px.line(df,x='year',y='cite',color='school_name')
fig
#%%

# fig.show(renderer='browser')
fig.write_image('distribution_per_year.png')
#%%
df_log=cite_per_year_df.groupby(['school_name','year']).cite.apply(lambda x:np.mean(np.log2(x))).reset_index()
fig=px.line(df_log,x='year',y='cite',color='school_name')
# fig.show(renderer='browser')
fig.layout.yaxis.title.text='Average cite per year (log)'
fig.write_image('distribution_per_year_log_scale.png')
#%%
school_name_order=cite_per_year_df.query('year == 2019').groupby('school_name').cite.median().sort_values().index
fig=px.box(cite_per_year_df.query('year >= 2010'),x='year',y='cite',color='school_name',log_y=False,hover_data=['year','cite','faculty_name'],category_orders={'school_name':school_name_order},range_y=[0,5000],width=3000,height=1000)
# fig=px.box(cite_per_year_df,x='year',y='cite',color='school_name',log_y=False,hover_data=['year','cite','faculty_name'],category_orders={'school_name':school_name_order},range_y=[0,5000])

fig.write_image('from 2010 boxplot.png',scale=3,)
fig.show()

#%% md
# increased
#%%
faculty_publication_df=faculty_publication_df.loc[:,['school_name', 'faculty_name', 'index', 'publication_year', 'num_citations',]]
faculty_publication_df.publication_year.astype(int)
faculty_publication_df.dropna(inplace=True)
# remove pub before 1980
faculty_publication_df.query('publication_year')


#%% md
### clean pub
#%%
