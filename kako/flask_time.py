
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from flask import Flask, render_template
import random
import os
import pandas as pd

path=os.path.dirname(os.path.abspath(__file__))+'/test.csv'

# データの読み込み
df = pd.read_csv(path,names=['time','num'],skiprows=[0],engine='python',index_col=[0],parse_dates=[0])
df.index.freq = 'H'
df.dropna().head()

app = Flask(__name__)

@app.route('/bokeh')
def bokeh():

    path=os.path.dirname(os.path.abspath(__file__))+'/yotei.csv'
    df = pd.read_csv(path)
    # datetime に変換する
    df["time"] = pd.to_datetime(df["time"])
    # ga:date を index として設定する 
    df.index = df["time"]

    #path2=os.path.dirname(os.path.abspath(__file__))+'/test2.csv'
    #df2 = pd.read_csv(path2)
    # datetime に変換する
    #df2["time"] = pd.to_datetime(df2["time"])
    # ga:date を index として設定する 
    #df2.index = df2["time"]


    p = figure(plot_width=800, plot_height=400, x_axis_type="datetime") 
    # add a line renderer
    p.line(df.index,df["num"], line_width=3,legend='num', color="red")
    #p.line(df2.index,df2["num"], line_width=3,legend='num', color="red")

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(p)
    html = render_template(
        'bokeh.html',
        title='マーシー',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)