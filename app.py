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
app = Flask(__name__);



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

  if Content == 'h':
    Content = tips
  else:
    try:
      for i in range(len(args)): args[i] = args[i].encode('utf8') # pass test
      Content = shark.feed( args )
      if Content == None : Content = error_msg
    except BaseException:
      Content = error_msg
  response = make_response( reply % (FromUserName, ToUserName, str(int(time.time())), Content ) )
  response.content_type = 'application/xml'
  return response

  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)