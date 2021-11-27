import datetime,time
isotime="2021-09-05T16:00:00Z"
isotime.getTime()

# st = datetime.datetime.sprptime(isotime,'%Y-%m-%dT%H:%M:%S%z')
# timestamp = int(time.mktime(st.timetuple()))
# print(timestamp)

now = time.time()  # 当前时间 float类型
print(time.strftime("%Y-%m-%d %H:%M:%S")  )#当前时间 str


time.ctime()   # 当前时间 english str


time.time()


print(time.localtime()  ) # 当前时间 time结构体

# time.struct_time(tm_year=2016, tm_mon=11, tm_mday=4, tm_hour=15, tm_min=26, tm_sec=9, tm_wday=4, tm_yday=309, tm_isdst=0)

print(time.localtime())  # float -> struct_time

# time.struct_time(tm_year=2016, tm_mon=11, tm_mday=4, tm_hour=15, tm_min=26, tm_sec=1, tm_wday=4, tm_yday=309, tm_isdst=0)

print(time.strftime('%Z 2021-09-05T16:00:00Z', time.localtime())  ) # 显示当前时区 China standard timezone

print(time.gmtime() )   # 显示UTC标准时间 跟中国相差8个钟

# time.struct_time(tm_year=2016, tm_mon=11, tm_mday=4, tm_hour=7, tm_min=26, tm_sec=28, tm_wday=4, tm_yday=309, tm_isdst=0)
