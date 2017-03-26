# encoding: UTF-8
period_dict={1: u'201101',
 2: u'201102',
 3: u'201103',
 4: u'201104',
 5: u'201105',
 6: u'201106',
 7: u'201107',
 8: u'201108',
 9: u'201109',
 10: u'201110',
 11: u'201111',
 12: u'201112',
 13: u'201201',
 14: u'201202',
 15: u'201203',
 16: u'201204',
 17: u'201205',
 18: u'201206',
 19: u'201207',
 20: u'201208',
 21: u'201209',
 22: u'201210',
 23: u'201211',
 24: u'201212',
 25: u'201301',
 26: u'201302',
 27: u'201303',
 28: u'201304',
 29: u'201305',
 30: u'201306',
 31: u'201307',
 32: u'201308',
 33: u'201309',
 34: u'201310',
 35: u'201311',
 36: u'201312',
 37: u'201401',
 38: u'201402',
 39: u'201403',
 40: u'201404',
 41: u'201405',
 42: u'201406',
 43: u'201501',
 44: u'201502',
 45: u'201503',
 46: u'201504',
 47: u'201505',
 48: u'201506',
 49: u'201601',
 50: u'201602',
 51: u'201603',
 52: u'201604',
 53: u'201605',
 54: u'201606',
 55: u'201701'};



rank_data=[ 90358,  74460, 250248,  85265,  96026, 203816,  91677,  94878,
       167264,  89123, 101810, 145893,  92460,  99248, 121744,  83415,
       100403, 105462,  77191,  81472,  71604,  62207,  68660,  56522,
        50233,  61149,  54680,  53105,  63701,  57262,  59374,  65423,
        56196,  55899,  59544,  47039,  43069,  38355,  32934,  33781,
        33443,  29446,  27552,  26455,  25208,  23054,  22558,  21082,
        19994,  20418,  20722,  20645,  20066,  16385,  12115]

total_count= sum(rank_data)
forward_str=u'''
非商业性质转载，请在文章开头标注：转载自《沙漠之鹰》，并在文末添加沙漠之鹰公众号二维码
若为商业性转载，请务必联系沙漠君本人，否则造成的一切后果请自行承担'''

history_str=u'''http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzIzMTAxNDQyNA==#wechat_webview_type=1&wechat_redirect'''
good_str=u'''http://mp.weixin.qq.com/mp/homepage?__biz=MzIzMTAxNDQyNA==&hid=1&sn=2a5bbab9a95b6a5a050e0bec2c43b53d#wechat_redirect'''

help_str=u'''可以回复:
【北京机动车13位编码】机动车摇号状态
【自住房 姓名】自住房摇号历史
【历史】 沙漠之鹰历史文章
【转载】 转载要求
【精选】 沙漠君的作战地图
【帮助】 显示帮助信息
'''

other_str=u'沙漠君会尽快给您回复,另可回复【帮助】查看自动回复方法'

zizhu_help =u"自住房摇号，请使用'自住房 姓名'来查询，谢谢"

res_dict={u'转载':forward_str,u'历史':history_str,u'帮助':help_str,u'精选':good_str}
