import time
now = int(1647267973000/1000)
time_value = time.localtime(int(1647267973000/1000))
print(time.strftime("%Y-%m-%d-%H", time.localtime(int(1647267973000/1000))))

import time

# 获得当前时间时间戳
# now = int(int(1647267973000/1000))
# # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
# timeArray = time.localtime(now)
# otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
# print(time.strftime("%Y-%m-%d %H:%M:%S", timeArray))