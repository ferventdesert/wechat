# encoding: UTF-8
import os;
import json
import cStringIO
from flask import Flask,  request, make_response
import hashlib
from flask import request
from lxml import etree
import xml.etree.ElementTree as ET
import time
from data import *
from pandas.io import sql
import pandas as pd
app = Flask(__name__);

import sqlite3

tips=u'你好啊'
con=None
#users= pd.read_hdf('yaohao.h5','user');
#users['lost']= users['lost'].map(lambda x:' '.join([str(r) for r in x]))
con=sqlite3.connect('yaohao.sqlite')
#con.execute('drop table if exists users')
#sql.to_sql(users,'users',con)
#con.execute('create index users_id on users(id)')
#con.close()


def get_int(x):
    try:
        x=int(x)
        return x
    except Exception as e:
        return 0;

import  codecs
log_file= codecs.open('input.log','w',encoding='utf-8')

@app.route('/', methods = ['GET', 'POST'] )
def wechat_auth():
  if request.method == 'GET':
    token = 'abc725527725527'
    query = request.args
    signature = query.get('signature', '')
    timestamp = query.get('timestamp', '')
    nonce = query.get('nonce', '')
    echostr = query.get('echostr', '')
    s = [timestamp, nonce, token]
    s.sort()
    s = ''.join(s)
    if ( hashlib.sha1(s).hexdigest() == signature ):
      return make_response(echostr)
  # Get the infomations from the recv_xml.
  xml_recv = ET.fromstring(request.data)
  ToUserName = xml_recv.find("ToUserName").text
  FromUserName = xml_recv.find("FromUserName").text
  Content = xml_recv.find("Content").text
  reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
  result=''
  if Content == 'h':
    result = tips
  else:
      try:
          result=get_response(Content);
          log_file.write(Content+'\n')
      except Exception as e:
          import traceback
          traceback.print_exc()
          result = u'沙漠君设计的程序不是很靠谱诶';
  response = make_response( reply % (FromUserName, ToUserName, str(int(time.time())),result ) )
  response.content_type = 'application/xml'
  return response

def get_type(text):
  import re
  if text in res_dict:
      return text,res_dict[text];

  num=re.compile('\\d{13}')
  res=num.search(text);
  if res is not None:
      return 'yaohao',res.group(0);
  else:
      return u'其他',other_str;
def get_response(text):
    mtype=get_type(text)
    if mtype[0]=='yaohao':
        return get_yaohao(mtype[1])
    else:
        return mtype[1]


def get_yaohao(id):
    columns=['index','id','start','end','period','count','selected','lost']
    res=con.execute('select * from users where id=%s'%(id))
    res = res.fetchone()
    if res is None:
        return u'没有找到您要查询的用户';
    else:
        dic = dict(zip( columns,res))
        #dic={'count': 31, 'end': 49, 'lost': [25, 26, 27, 34, 35, 50, 51], 'selected': 0, 'period': 26, 'start': 19, 'id': '5606101836469'}
    #print dic;
    start= int(dic['start'])
    end=int(dic['end'])
    period= int(dic['period']);
    dic['start']= period_dict[dic['start']];
    dic['select']= u'恭喜摇中!摇中了还查什么...' if dic['selected']==1 else u'还没有摇中/(ㄒoㄒ)/'
    lost_count=end-start+1-period
    if lost_count==0:
        dic['lost']=u'您没有拉下一次摇号!'
    else:
        lost_period=u'【' + ' '.join( period_dict[get_int(r)] for r in  dic['lost'].split(' ') if r.strip()!='')+u'】';
        dic['lost']= u'期间中断了{lost_count}期,分别是{lost}'.format(lost_count=lost_count,lost=lost_period);

    dic['ratio']= get_int(get_int(dic['count'])/6.0);
    dic['percent']= round(dic['count']/6.0/991.0,5);
    res= u'您的编号{id}\n在{start}期开始摇号,总计{count}次,{select}\n{lost}\n目前中签倍率为{ratio}倍, 下期摇中概率{percent}'.format(**dic);
    return res;

if __name__ == '__main__':
    # print get_response(u'历史')
    # print get_response(u'帮助')
    # print get_response(u'转载')
    print get_response(u'5935104232928')
    print get_response(u'5606101836469')
    #exit()
    app.run(host='0.0.0.0', port=80, debug=False)
    con.close()
    log_file.close()
