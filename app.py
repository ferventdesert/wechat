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
from data import period_dict
import pandas as pd
app = Flask(__name__);


DEBUG=True
tips=u'你好啊'
print ('start load data')
if not DEBUG:
    users= pd.read_hdf('yaohao.h5','user');
    users.index= users.id
print ('data loaded')

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
      except BaseException:
          result = u'您的输入有误';
  response = make_response( reply % (FromUserName, ToUserName, str(int(time.time())),result ) )
  response.content_type = 'application/xml'
  return response

def get_type(text):
  import re
  num=re.compile('\\d{13}')
  res=num.search(text);
  if res is not None:
      return 'yaohao',res.group(0);
def get_response(text):
    mtype=get_type(text)
    if mtype[0]=='yaohao':
        return get_yaohao(mtype[1])

def get_yaohao(id):
    if not DEBUG:
        u=users.ix[id];
        if u is None:
            return u'没有找到您要查询的用户';
        dic=u.to_dict();
    else:
        dic={'count': 31, 'end': 49, 'lost': [25, 26, 27, 34, 35, 50, 51], 'selected': 0, 'period': 26, 'start': 19, 'id': '5606101836469'}
    #print dic;
    dic['start']= period_dict[dic['start']];
    dic['select']= u'已经摇中' if dic['selected']==1 else u'还没有摇中'
    dic['lost_count']=len(dic['lost']);
    dic['lost']= ' '.join( period_dict[r] for r in  dic['lost']);
    dic['percent']= 1.0//1000;

    res= u'您的编号{id},在{start}期开始摇号,总计{count}次,{select}\n中间中断了{lost_count}期,分别是{lost} \n目前摇号概率为{percent}'.format(**dic);
    return res;

if __name__ == '__main__':
    print get_response('5606101836469')
    if DEBUG:
        exit()
    app.run(host='0.0.0.0', port=80, debug=False)