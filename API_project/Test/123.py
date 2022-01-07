import datetime,time,random
isotime="2021-09-05T16:00:00Z"
# isotime.getTime()
# print(random.randint(100,999))
# st = datetime.datetime.sprptime(isotime,'%Y-%m-%dT%H:%M:%S%z')
# timestamp = int(time.mktime(st.timetuple()))
# print(timestamp)

now = time.time()  # 当前时间 float类型
print(time.strftime("%Y-%m-%d %H:%M:%S")  )#当前时间 str
print(time.strftime("%Y年%m月%d日%H时%M分")  )#当前时间 str
print(time.strftime("%Y_%m_%d_%H_%M_%S")  )#当前时间 str

# time.sleep(3)
#
# time.ctime()   # 当前时间 english str
#
#
# time.time()
#
#
# print(time.localtime()  ) # 当前时间 time结构体
#
# # time.struct_time(tm_year=2016, tm_mon=11, tm_mday=4, tm_hour=15, tm_min=26, tm_sec=9, tm_wday=4, tm_yday=309, tm_isdst=0)
#
# print(time.localtime())  # float -> struct_time
#
# # time.struct_time(tm_year=2016, tm_mon=11, tm_mday=4, tm_hour=15, tm_min=26, tm_sec=1, tm_wday=4, tm_yday=309, tm_isdst=0)
#
# print(time.strftime('%Z 2021-09-05T16:00:00Z', time.localtime())  ) # 显示当前时区 China standard timezone
#
# print(time.gmtime() )   # 显示UTC标准时间 跟中国相差8个钟

# time.struct_time(tm_year=2016, tm_mon=11, tm_mday=4, tm_hour=7, tm_min=26, tm_sec=28, tm_wday=4, tm_yday=309, tm_isdst=0)
# time_name = time.strftime("%Y-%m-%d %H:%M:%S").split(":")[0].replace("-", "_").replace(" ", "_")
# time_name1 = time.strftime("%Y-%m-%d %H:%M:%S").replace("-", "_").replace(" ", "_").replace(":", "*")
# print(time_name1.replace('*',''))#当前时间 str
# print(time_name.split(":"))#当前时间 str
# s = 'abc:123'
# # 字符串拼接方式去除冒号
# new_s = s[:3] + s[4:]
# print(new_s)
# # !/usr/bin/python3
# # 去除字符串中相同的字符
# s = '\tabc\t123\tisk'
# print(s.replace('\t', ''))
# import re
# # 去除\r\n\t字符
# s = '\r\nabc\t123\nxyz'
# print(re.sub('[\r\n\t]', '', s))
# 去两边空格：str.strip()
# 去左空格：str.lstrip()
# 去右空格：str.rstrip()
# 去两边字符串：str.strip('d')，相应的也有lstrip，rstrip
# str=' python String function '
# print ('%s strip=%s' % (str,str.strip()))
# str='python String function'
# print ('%s strip=%s' % (str,str.strip('d')))

# 按指定字符分割字符串为数组：str.split(' ')
from API_project.Configs.config_API import configuration_file
HOST = "test"
staticConfig = configuration_file(HOST).staticConfig()['contactSiteSourceMap']  # 实例化高级搜索配置withLevels并返回配置信息
staticConfig_list = []
for staticConfig_value in staticConfig:
    staticConfig_list = staticConfig_list + staticConfig_value['sub']
sum = 0
for i in staticConfig_list:
    sum+=1
    # if i["value"] == "康强":
    #     break
print(sum)