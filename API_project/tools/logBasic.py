# -*- coding: utf-8 -*-
# @File    : logBasic.py
# @Time    : 2021/6/6 10:46
# @Author  : xintian
# @Email   : 1730588479@qq.com
# @Software: PyCharm
# Date:2021/6/6
import logging
import datetime


# 原则：适用就行
def logger(name=__name__):  # 当前模块名
    # 1- 日志名称：路径+名字+后缀名
    logName = f"../logs/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.log"
    # 2- 创建日志对象
    logObject = logging.getLogger(name)
    # 3- 日志级别----性能测试--有时候需要关注日志的级别
    logObject.setLevel(logging.INFO)
    # 4- 日志属性
    rHandler = logging.FileHandler(logName, mode="w", encoding="utf-8")
    # 5- 日志内容格式
    # 2021-06-03 18:21:16,133 INFO o.a.j.u.JMeterUtils: Setting Locale
    formater = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[%(lineno)d]:%(message)s")
    rHandler.setFormatter(formater)
    logObject.addHandler(rHandler)

    return logObject  # 日志的实例


if __name__ == '__main__':
    log = logger()
    log.error("---我出现错误了---")
