
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from flask import Flask, render_template, request
import random
import csv
import os
import pandas as pd
import make_yotei
import shutil
from datetime import datetime
import CT_bunseki


app = Flask(__name__)
path=os.path.dirname(os.path.abspath(__file__))

#初期値の設定画面
@app.route('/ini', methods = ["GET", "POST"])
def ini():
   #設定更新時に 更新情報をini.csvに登録
   if request.method == 'POST':
      with open(path+'/ini.csv','w') as f:
         writer = csv.writer(f)
         writer.writerow(['項目','値1','値2'])
         writer.writerow(['標準CT',request.form.get('H_CT')])
         writer.writerow(['閾値CT',request.form.get('S_CT')])
         writer.writerow(['就業時間',request.form.get('worktime_start'),request.form.get('worktime_end')])
         for i in range(9):
            writer.writerow(['休憩時間'+str(i+1),request.form.get('kyukeiS_'+str(i+1)),request.form.get('kyukeiE_'+str(i+1))])
      make_yotei.yotei()
   
   #設定画面表示
   df = pd.read_csv(path+'/ini.csv', header=0, index_col=0)
   print (df)
   print (df.iloc[3:10,:])
   html = render_template(
      'ini.html',
      H_CT=df.loc['標準CT','値1'],
      S_CT=df.loc['閾値CT','値1'],
      worktime_start=df.loc['就業時間','値1'],
      worktime_end=df.loc['就業時間','値2'],
      kyukei=df.iloc[3:10,:].values.tolist()
   )
   return encode_utf8(html)

   
#グラフ表示
@app.route('/bokeh')
def bokeh():
   path=os.path.dirname(os.path.abspath(__file__))
   df = pd.read_csv(path+'/yotei/yotei.csv')
   # datetime に変換する
   df["time"] = pd.to_datetime(df["time"])
   # ga:date を index として設定する 
   df.index = df["time"]
   p = figure(plot_width=1200, plot_height=300, x_axis_type="datetime") 
   # add a line renderer
   p.line(df.index,df["num"], line_width=3,legend='num', color="green")


   now=datetime.now()
   log_name='{:%Y-%m-%d}_{}.csv'.format(now,2)
   path2=path+'/bunseki/CT_'+log_name
   if os.path.exists(path+'/bunseki/CT_'+log_name):
      df2 = pd.read_csv(path2)
      # datetime に変換する
      df2["開始"] = pd.to_datetime(df2["開始"])
      # ga:date を index として設定する 
      df2.index = df2["開始"]
      p.line(df2.index,df2["実績数"], line_width=3,legend='実績数', color="blue")

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

#センサー情報を取得し、logに保存する
@app.route('/log', methods = ["GET", "POST"])
def log():
   if request.method == 'POST':
      id = request.form.get("id")

      now=datetime.now()
      log_name='{:%Y-%m-%d}_{}.csv'.format(now,id)
      if os.path.exists(path+'/log/'+log_name):
         with open(path+'/log/'+log_name, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([id,now,1])
      else:
         with open(path+'/log/'+log_name, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['id','time','X'])
            writer.writerow([id,now,1])
         with open(path+'/bunseki/CT_'+log_name, 'w') as f1:
            fieldnames = ['id', '開始','終了','CT','就業時間判定','休憩時間判定','実績数']
            writer = csv.DictWriter(f1, fieldnames=fieldnames)
            writer.writeheader()
      CT_bunseki.syoki(log_name)
   
   html = render_template(
      'log.html',
   )
   return encode_utf8(html)
   
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)