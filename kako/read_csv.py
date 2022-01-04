import pandas as pd
import datetime
import os

from bokeh.plotting import figure, output_notebook, show
from bokeh.models import ColumnDataSource, LabelSet

path=os.path.dirname(os.path.abspath(__file__))+'/test.csv'
df = pd.read_csv(path)
# datetime に変換する
df["time"] = pd.to_datetime(df["time"])
# ga:date を index として設定する 
df.index = df["time"]

path2=os.path.dirname(os.path.abspath(__file__))+'/test2.csv'
df2 = pd.read_csv(path2)
# datetime に変換する
df2["time"] = pd.to_datetime(df2["time"])
# ga:date を index として設定する 
df2.index = df2["time"]


p = figure(plot_width=800, plot_height=400, x_axis_type="datetime") 
# add a line renderer
p.line(df.index,df["io"], line_width=3,legend='io', color="red")
p.line(df2.index,df2["io"], line_width=3,legend='io', color="red")

# 表示
show(p)