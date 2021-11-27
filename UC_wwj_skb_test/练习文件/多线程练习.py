import time
import os
import threading


def open_calc():
    with open('test.txt', 'r') as f:
        for line in f.readlines():
            while 'hello' in line:
                os.system("calc.exe")
                # 如果字符串已经出现并已经执行命令，则终止程序，否则会一直执行命令
                return
        # 等for循环判断完没有标识后再休眠重新调用该函数
        print('没有找到启动标识：hello，等5秒再检测')
        time.sleep(5)
        # 再次调用函数
        open_calc()


def open_mstsc():
    with open('test.txt', 'r') as f:
        for line in f.readlines():
            while 'abc' in line:
                os.system("mstsc.exe")
                # 如果字符串已经出现并已经执行命令，则终止程序，否则会一直执行命令
                return
        # 等for循环判断完没有标识后再休眠重新调用该函数
        print('没有找到启动标识：abc，等6秒再检测')
        time.sleep(6)
        # 再次调用函数
        open_mstsc()



if __name__ == '__main__':
    # 使用threading模块，threading.Thread()创建线程，其中target参数值为需要调用的方法，同样将其他多个线程放在一个列表中，遍历这个列表就能同时执行里面的函数了
    threads = [threading.Thread(target=open_calc),
               threading.Thread(target=open_mstsc)]
    for t in threads:
        # 启动线程
        t.start()