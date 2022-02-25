# import datetime, time, random
#
# isotime = "2021-09-05T16:00:00Z"
# # isotime.getTime()
# # print(random.randint(100,999))
# # st = datetime.datetime.sprptime(isotime,'%Y-%m-%dT%H:%M:%S%z')
# # timestamp = int(time.mktime(st.timetuple()))
# # print(timestamp)
# # format_time = "2017-03-16 18:22:06"
# # ts = time.strptime(format_time, "%Y-%m-%d %H:%M:%S")
# # print(time.mktime(ts))
# format_time = "2021-03-05"
# ts = time.strptime(format_time, "%Y-%m-%d")
# print(ts)
# a = time.mktime(ts)
# print(a)
# c = time.time()
# b = 24*60*60
# print(a)
# print(c)
# print(b)
# print((c-a))
# # print(time.time()-time.mktime(ts))
#
# e = (c-a) / b
# print(e)
# print(list(range(2,10)))
# print(round(e))
#
# aa = round(5.5 // 2)
#
# cc = round(5.5 / 2,2)
# print(aa)
# if cc > aa:
#     print(1234)
# print(round(5.5 / 2,2))
# # iplist = list(range(0,2000))
# # for index in range(0, len(iplist), 200):
# #     item_list = iplist[index:index + 200]
# #     print(item_list)
# # now = time.time()  # 当前时间 float类型
# print(time.mktime(ts))
# # print(now)
# # print(time.strftime("%Y-%m-%d %H:%M:%S"))  # 当前时间 str
# # print(time.strftime("%Y年%m月%d日%H时%M分"))  # 当前时间 str
# # print(time.strftime("%Y_%m_%d_%H_%M_%S"))  # 当前时间 str
# # a = [{"shanghai": "keji1"}]
# # time.sleep(3)
# #
# # time.ctime()   # 当前时间 english str
# #
# #
# # time.time()
# #
# #
# # print(time.localtime()  ) # 当前时间 time结构体
# #
# # # time.struct_time(tm_year=2016, tm_mon=11, tm_mday=4, tm_hour=15, tm_min=26, tm_sec=9, tm_wday=4, tm_yday=309, tm_isdst=0)
# #
# # print(time.localtime())  # float -> struct_time
# #
# # # time.struct_time(tm_year=2016, tm_mon=11, tm_mday=4, tm_hour=15, tm_min=26, tm_sec=1, tm_wday=4, tm_yday=309, tm_isdst=0)
# #
# # print(time.strftime('%Z 2021-09-05T16:00:00Z', time.localtime())  ) # 显示当前时区 China standard timezone
# #
# # print(time.gmtime() )   # 显示UTC标准时间 跟中国相差8个钟
#
# # time.struct_time(tm_year=2016, tm_mon=11, tm_mday=4, tm_hour=7, tm_min=26, tm_sec=28, tm_wday=4, tm_yday=309, tm_isdst=0)
# # time_name = time.strftime("%Y-%m-%d %H:%M:%S").split(":")[0].replace("-", "_").replace(" ", "_")
# # time_name1 = time.strftime("%Y-%m-%d %H:%M:%S").replace("-", "_").replace(" ", "_").replace(":", "*")
# # print(time_name1.replace('*',''))#当前时间 str
# # print(time_name.split(":"))#当前时间 str
# # s = 'abc:123'
# # # 字符串拼接方式去除冒号
# # new_s = s[:3] + s[4:]
# # print(new_s)
# # # !/usr/bin/python3
# # # 去除字符串中相同的字符
# # s = '\tabc\t123\tisk'
# # print(s.replace('\t', ''))
# # import re
# # # 去除\r\n\t字符
# # s = '\r\nabc\t123\nxyz'
# # print(re.sub('[\r\n\t]', '', s))
# # 去两边空格：str.strip()
# # 去左空格：str.lstrip()
# # 去右空格：str.rstrip()
# # 去两边字符串：str.strip('d')，相应的也有lstrip，rstrip
# # str=' python String function '
# # print ('%s strip=%s' % (str,str.strip()))
# # str='python String function'
# # print ('%s strip=%s' % (str,str.strip('d')))
#
# # 按指定字符分割字符串为数组：str.split(' ')
# # from API_project.Configs.config_API import configuration_file
# # HOST = "test"
# # staticConfig = configuration_file(HOST).staticConfig()['contactSiteSourceMap']  # 实例化高级搜索配置withLevels并返回配置信息
# # staticConfig_list = []
# # for staticConfig_value in staticConfig:
# #     staticConfig_list = staticConfig_list + staticConfig_value['sub']
# # sum = 0
# # for i in staticConfig_list:
# #     sum+=1
# #     if i["value"] == "企一网":
# #         break
# # print(sum)
# # businessscope="<em>机电</em>设备<em>工程</em>，制冷<em>空调</em>设备<em>工程</em>，水电安装，中央<em>空调</em>维修服务，<em>机电</em>设备，制冷<em>空调</em>设备，计算机、软件及辅助设备销售，建设<em>工程</em>项目管理咨询。"
# # a = "中医 诊所"
# # b = "深圳弘坤堂中医（综合）诊所"
# # c = businessscope.replace('，','').replace('/','').replace('、','').replace('。','').strip("<em>").split("<em>")
# # print(list(set(c)))
# # d = list(set(c))
# # aa = ('制冷', '工程', '机电', '水电安装中央', '空调', '维修服务', '设备', '设备制冷', '设备计算机软件及辅助设备销售建设', '项目管理咨询')
# # cc = ('制冷', '机电', '工程', '水电安装中央', '空调', '维修服务', '设备', '设备制冷', '设备计算机软件及辅助设备销售建设', '项目管理咨询')
# # d.sort()
# #
# # print(aa == cc)
# # print(','.join(d))
# # socialSecNum = "27418人"
# # print(socialSecNum.strip("人"))
# #
# # a = {'User-Agent': 'python-requests/2.26.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*',
# #      'Connection': 'keep-alive', 'platform': 'IK', 'usertoken': 'Token token=268e61a4c41e4be9d7be7c7bf90bf116',
# #      'Content-Type': 'application/json', 'crmplatformtype': 'lixiaoyun'}
# # content_list_type1 = []
# # print(len(content_list_type1))
# import time
# timeStamp = 1271779200
#
# # timeArray = time.localtime(timeStamp)
#
# otherStyleTime = time.strftime("%Y-%m-%d", time.localtime(timeStamp))
#
# print(otherStyleTime)  # 2013--10--10 23:40:00

a = [1,2,3,4,5]
print(a[:2:-1])