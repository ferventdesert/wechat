# encoding: UTF-8
import os;
import json
import cStringIO
from flask import Flask, request, make_response
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

tips = u'你好啊'
con = None
con = sqlite3.connect('yaohao.sqlite')


# @app.route('/')
# def root():
#    return app.send_static_file('index.html')

@app.route('/resources/<m_file>', methods=['GET'])
def get_static_file(m_file):
    print(m_file)
    return app.send_static_file('resources/' + m_file)


def get_int(x):
    try:
        x = int(x)
        return x
    except Exception as e:
        return 0;


import codecs

log_file = codecs.open('input.log', 'a', encoding='utf-8')


@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
    try:
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
            if (hashlib.sha1(s).hexdigest() == signature):
                #  return make_response(echostr)
                return echostr
                # Get the infomations from the recv_xml.
        xml_recv = ET.fromstring(request.data)
        ToUserName = xml_recv.find("ToUserName").text
        FromUserName = xml_recv.find("FromUserName").text
        Content = xml_recv.find("Content").text
        reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        result = ''
        if Content == 'h':
            result = tips
        else:
            result = get_response(Content);
            log_file.write(Content + '\n')
    except Exception as e:
        import traceback
        traceback.print_exc()
        result = u'沙漠君设计的程序不是很靠谱诶';
    response = make_response(reply % (FromUserName, ToUserName, str(int(time.time())), result))
    response.content_type = 'application/xml'
    return response


def get_type(text):
    import re
    if text in res_dict:
        return text, res_dict[text];
    if text.startswith(u'自住'):
        user = [r.strip() for r in text.split(' ') if r != '']
        if len(user) < 2:
            return u'其他', zizhu_help
        return 'zizhu', user[1]

    num = re.compile('\\d{13}')
    res = num.search(text);
    if res is not None:
        return 'yaohao', res.group(0);
    else:
        return u'其他', other_str;


def get_response(text):
    mtype = get_type(text)
    if mtype[0] == 'yaohao':
        return get_yaohao(mtype[1])
    elif mtype[0] == 'zizhu':
        return get_zizhu(mtype[1])
    else:
        return mtype[1]


def get_yaohao(id):
    columns = ['index', 'id', 'start', 'end', 'period', 'count', 'selected', 'lost']
    res = con.execute('select * from users where id="%s"' % (id))
    res = res.fetchone()
    if res is None:
        return u'没有找到您要查询的用户';
    else:
        dic = dict(zip(columns, res))
        # dic={'count': 31, 'end': 49, 'lost': [25, 26, 27, 34, 35, 50, 51], 'selected': 0, 'period': 26, 'start': 19, 'id': '5606101836469'}
    # print dic;
    start = int(dic['start'])
    end = int(dic['end'])
    period = int(dic['period']);
    dic['start'] = period_dict[dic['start']];
    dic['select'] = u'恭喜摇中!摇中了还查什么...' if dic['selected'] == 1 else u'还没有摇中/(ㄒoㄒ)/'
    lost_count = end - start + 1 - period
    dic['lost_count'] = lost_count
    if lost_count == 0:
        dic['lost'] = u'您没有落下一次摇号!'
    else:
        arr = [period_dict[get_int(r)] for r in dic['lost'].split(' ') if r.strip() != '']
        lost_period = u'【' + ' '.join(arr) + u'】';
        dic['lost'] = u'期间中断了{lost_count}期,分别是{lost}'.format(lost_count=len(arr), lost=lost_period);

    ratio = get_int(get_int(dic['period']) / 6.0) + 1

    if ratio > 9:
        ratio = 9
    dic['ratio'] = ratio
    dic['percent'] = int(round(1 / (ratio * 0.00126 * 6), 0)) * 0.6
    dic['rank'] = 100 - int(sum(rank_data[i] for i in range(period)) / float(total_count) * 100.0)
    dic['id0'] = int(dic['id'][-7:])
    res = u'您从{start}期开始摇号,第{id0}个申请者，优先级排名前{rank}%，共摇了{period}期,出现{count}次,{select}\n{lost}\n目前中签倍率为{ratio}倍, 预计摇中需{percent}年'.format(
        **dic);
    return res


def get_zizhu(user):
    result = ''
    if len(user) < 5:
        res = con.execute('select _name,_type, _index,_rank from zizhu where _user="%s"' % (user))
    else:
        res = con.execute('select _name,_type, _index,_rank from zizhu where _index="%s"' % (user))
    columns = [u'name', u'type', u'index', u'rank']

    res = res.fetchall()
    if res is None:
        return u'没有找到您要查询的用户';
    else:
        dic_list = {}

        for r in res:

            index = r[2]
            dic = dict(zip(columns, r))
            if index not in dic_list:
                dic_list[index] = [dic]
            else:
                dic_list[index].append(dic)

        result += u"查询'{0}',共有{1}个编码:\n".format(user, len(dic_list))
        if len(dic_list) > 20:
            result += u'重名人数过多,仅输出前50个编码,请输入【自住房 编码】查询\n' + '\n'.join(sorted(dic_list.keys()[:50]))
            return result

        string = u'  {name},{type},排名{rank}\n'

        for k, v in dic_list.items():
            result += u'申请编码:' + k + '\n'
            for vv in v:
                result += string.format(**vv)
        return result


if __name__ == '__main__':
    print get_response(u'历史')
    print get_response(u'帮助')
    print get_response(u'转载')

    print get_response(u'0203101800247')
    print get_response(u'5606101836469')
    print get_response(u'自住房 张睿')
    exit()
    print get_response(u'自住房 王伟')
    print get_response(u'自住房 9179001681472')
    app.run(host='0.0.0.0', port=80, debug=False)
    con.close()
    log_file.close()
