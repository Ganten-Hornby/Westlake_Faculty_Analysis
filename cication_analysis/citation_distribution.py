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
school_total_path=Path(r'F:\0_Desktop\Citation_Analysis\result\total\school_total.json')
school_total=json.load(school_total_path.open())

#%%

