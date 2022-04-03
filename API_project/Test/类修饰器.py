# 修饰器定义：
#
# 英文名叫Decorator，主要用来对功能函数进行润色，在原有功能的基础上添加一些额外修饰。有些地方也叫做切面函数，即对功能函数切面穿插新功能。修饰器能减少代码冗余重复，使整体风格更加优雅高效。
#
# 常用场景：函数调用日志，函数性能统计，函数异常捕获，函数认证访问控制等。
#
# 使用方法：就是在方法名前面加一个 @ XXX注解来为这个方法装饰一些东西。
#
# 1，不带参数的修饰器


##在函数调用前后答应调用记录
def func_decorator(func):
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        print(' '.join(["before", func_name, "is called"]))
        resp = func(*args, **kwargs)
        print(' '.join(["after", func_name, "is called"]))
        return resp

    return wrapper


@func_decorator  ##@func_decorator即为我们预先定义的修饰器
def test_01(*args, **kwargs):  ##功能函数
    print(args)
    print(kwargs)


test_01("hello", "welcome")
# 运行后，我们将看到如下输出：
#
# before
# test_01 is called
# ('hello', 'welcome')
# {}
# after
# test_01 is called
# 修饰器 @ func_decorator功能等同于func = func_decorator(func)
#
# 其效果和如下实现相同


##在函数调用前后答应调用记录
def func_decorator(func):
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        print(' '.join(["before", func_name, "is called"]))
        resp = func(*args, **kwargs)
        print(' '.join(["after", func_name, "is called"]))
        return resp

    return wrapper


# @func_decorator ##@func_decorator等同于func = func_decorator(func)
def test_01(*args, **kwargs):  ##功能函数
    print(args)
    print(kwargs)


# test_01("hello", "welcome")

func_decorator(test_01)("hello", "welcome")
# 2，多个修饰器

import time


##在函数调用前后答应调用记录
def func_decorator_call(func):
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        print(' '.join(["before", func_name, "is called"]))
        resp = func(*args, **kwargs)
        print(' '.join(["after", func_name, "is called"]))
        return resp

    return wrapper


def func_decorator_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(' '.join(["before", str(start_time), " func start"]))
        resp = func(*args, **kwargs)
        end_time = time.time()
        print(' '.join(["after", str(end_time), "func end"]))
        return resp

    return wrapper


@func_decorator_call
@func_decorator_time  ###多个修饰器是按照由内到外的顺序，即最外层的修饰效果出现在最外层
def test_01(*args, **kwargs):  ##功能函数
    print(args)
    print(kwargs)


test_01("hello", "welcome")
# 输出：
#
# before
# wrapper is called
# before
# 1536406178.534688
# func
# start
# ('hello', 'welcome')
# {}
# after
# 1536406178.534733
# func
# end
# after
# wrapper is called
# 3，带参数的修饰器


def func_decorator_with_param(dec_tag, *dec_args, **dec_kwargs):  ##修饰器参数
    print(" ".join(["the outer decorator tag :", dec_tag]))

    def decorator(func):  ##返回外层修饰器
        start_time = time.time()
        print(' '.join(["func start: ", str(start_time)]))

        def wrapper(*args, **kwargs):  ##内层封装
            resp = func(*args, **kwargs)
            return resp

        print(' '.join(["func params: ", str(dec_args), str(dec_kwargs)]))
        return wrapper

    return decorator


@func_decorator_with_param(dec_tag="outer_tag", demo="decorator with param")
def test_02(*args, **kwargs):  ##功能函数
    print(args)
    print(kwargs)


test_02("hello", "welcome")
# 输出：
#
# the
# outer
# decorator
# tag: outer_tag
# func
# start: 1536407272.8988101
# func
# params: ()
# {'demo': 'decorator with param'}
# ('hello', 'welcome')
# {}
# 4，class风格的修饰器
#
# (1)
# 不带参数的修饰器


class DecoratorDemo(object):
    def __init__(self, func):
        self.func = func
        print(' '.join([func.__name__, "is init"]))

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


@DecoratorDemo
def test_03(*args, **kwargs):  ##功能函数
    print(args)
    print(kwargs)


test_03("hello", "welcome")
# 输出：
#
# test_03 is init
# ('hello', 'welcome')
# {}
# (2)
# 带参数的修饰器
#
# 如果decorator有参数的话，__init__()
# 成员就不能传入func了，而func是在__call__的时候传入的


class DecoratorDemo(object):
    def __init__(self, dec_tag, *dec_args, **dec_kwargs):
        self.dec_tag = dec_tag
        self.dec_args = dec_args
        self.dec_kwargs = dec_kwargs
        print(' '.join([dec_tag, "decorat with params "]))

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print(' '.join([func.__name__, "is called"]))
            print(' '.join([self.dec_tag, "is a dec_tag"]))
            resp = func(*args, **kwargs)
            print(' '.join(["func params: ", str(self.dec_args), str(self.dec_kwargs)]))
            return resp

        return wrapper


@DecoratorDemo(dec_tag="outer_tag", demo="decorator with param")
def test_03(*args, **kwargs):  ##功能函数
    return "hello, arg is {0}, kwargs is {1}".format(args, kwargs)


result = test_03("hello", "welcome")
print(result)
# 输出：
#
# outer_tag
# decorat
# with params
#     test_03 is called
# outer_tag is a
# dec_tag
# func
# params: ()
# {'demo': 'decorator with param'}
# hello, arg is ('hello', 'welcome'), kwargs is {}
# 5，类里面使用修饰器
#
# (1)
# 不需要依赖class内部方法


## 异常处理不需要依赖class内部方法
def catch_exception_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            resp = func(*args, **kwargs)
            return resp
        except Exception:
            print(" do something no need class method")
    return wrapper


class DemoMudule(object):
    def __init__(self):
        pass

    def do_more_something(self):
        print("do something in class")

    @catch_exception_decorator
    def test_05(self, *args, **kwargs):
        print(str(args) + str(kwargs))
        print('1' + str(args))
        return str(args) + str(kwargs)


demo_test5 = DemoMudule().test_05(hello="welcome")
print(demo_test5)
# 输入：
#
# ()
# {'hello': 'welcome'}
# do
# something
# no
# need
# class method
#     None
# （2）需要依赖class内部方法
#
# 此时需要传入参数self


## 异常处理需要依赖class内部方法
def catch_exception_within_class_decorator(func):
    def wrapper(self, *args, **kwargs):
        try:
            resp = func(self, *args, **kwargs)
            return resp
        except Exception:
            self.do_more_something()
            # raise Exception

    return wrapper


class DemoMudule(object):
    def __init__(self):
        pass

    def do_more_something(self):
        print("do something in class")

    @catch_exception_within_class_decorator
    def test_04(self, *args, **kwargs):
        print(str(args) + str(kwargs))
        print('1' + str(args))
        return str(args) + str(kwargs)


demo_test4 = DemoMudule().test_04(hello="welcome")
print(demo_test4)
# 输出：
#
# ()
# {'hello': 'welcome'}
# do
# something in
#
#
# class
#     None

#
# 6，类修饰器
#
# 如果我们拥有
# scraper
# 类以及多个函数需要使用修饰器，此时需要给每个函数加上修饰器，代码显得冗余

from functools import wraps
import time
import random


def wait_random(min_wait=1, max_wait=30):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            time.sleep(random.randint(min_wait, max_wait))
            resp = func(self, *args, **kwargs)
            return resp

        return wrapper

    return decorator


class Scraper(object):
    @wait_random(min_wait=1, max_wait=2)
    def func_to_scrape_1(self):
        print("func_to_scrape_1")
        # some scraping stuff

    @wait_random(min_wait=1, max_wait=2)
    def func_to_scrape_2(self):
        print("func_to_scrape_2")
        # some scraping stuff

    @wait_random(min_wait=1, max_wait=2)
    def func_to_scrape_3(self):
        print("func_to_scrape_3")
        # some scraping stuff


instan = Scraper()
instan.func_to_scrape_1()
instan.func_to_scrape_2()
instan.func_to_scrape_3()
# 此时我们可以使用类修饰器。方法就是遍历类名称空间，确定函数，然后通过装饰器包装这些函数。

from functools import wraps
import time
import random


def wait_random(min_wait=1, max_wait=30):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            time.sleep(random.randint(min_wait, max_wait))
            resp = func(self, *args, **kwargs)
            return resp
        return wrapper
    return decorator


def class_wrapper(cls):
    attrs = vars(cls)  ##等同于cls.__dict__
    for name, val in attrs.items():
        if callable(val):
            setattr(cls, name, wait_random(min_wait=1, max_wait=2)(val))
    return cls


@class_wrapper
class Scraper(object):
    def func_to_scrape_1(self):
        print("func_to_scrape_1")
        # some scraping stuff

    def func_to_scrape_2(self):
        print("func_to_scrape_2")
        # some scraping stuff

    def func_to_scrape_3(self):
        print("func_to_scrape_3")
        # some scraping stuff


instan = Scraper()
instan.func_to_scrape_1()
instan.func_to_scrape_2()
instan.func_to_scrape_3()
# 类装饰器和函数装饰器类似，只不过类装饰器作用对象为类对象，对类做修饰或者拦截。
# 首先需要定义一个修饰器，该修饰器需要能接受class，并且保留class的所有属性
# （1）简单的类修饰器
# 给类添加修饰方法，即每次对类操作时执行一个默认修饰。如本例，每次操作类对象都打印log


def simple_class_decorator(obj):
    name = obj.__name__
    print(' '.join([name, "is used"]))
    return obj


@simple_class_decorator
class TestModule(object):
    def __init__(self):
        pass

    def do_something1(self):
        print("do something1")

    def do_something2(self):
        print("do something2")


test_instance1 = TestModule()
test_instance1.do_something1()

test_instance2 = TestModule()
test_instance2.do_something2()
# 输出：

# 给类增加额外的属性
# 方法一：

def add_class_attr_decorator(obj):
    obj.new_attr = "new attr"

    def new_func(*args, **kwargs):
        print(' '.join([str(args), str(kwargs)]))

    obj.new_func = new_func
    return obj


@add_class_attr_decorator
class TestModule(object):
    def __init__(self):
        pass

    def do_something1(self):
        print("do something1")


test_instance1 = TestModule()
print(test_instance1.new_attr)
test_instance1.new_func("hello", happy="happ welcome")
# 输出：

# {'happy': 'happ welcome'}
# 方法2:


def add_class_attr_decorator(*new_attrs):
    def class_decorator(cls):
        class ClassWrapper(cls):
            def __init__(self, *args, **kwargs):
                for new_attr in new_attrs:
                    setattr(self, new_attr, None)
                super(ClassWrapper, self).__init__(*args, **kwargs)

        return ClassWrapper

    return class_decorator


@add_class_attr_decorator("id", "name")
class TestModule(object):
    def __init__(self):
        pass

    def do_something1(self):
        print("do something1")

    def do_something2(self):
        print("do something2")


test_instance1 = TestModule()
test_instance1.id
test_instance1.name

# 给类中所有的方法添加修饰


def timeit_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(" ".join([func.__name__, " is calling "]))
        resp = func(*args, **kwargs)
        end_time = time.time()
        cost = end_time - start_time
        print(" ".join([func.__name__, "cost is:", str(cost)]))
        return resp

    return wrapper


def add_decorator_to_method_decorator(*method_names):
    def class_decorator(cls):
        class NewClassWrapper(cls):
            def __getattribute__(self, attr_name):
                attr_val = super(NewClassWrapper, self).__getattribute__(attr_name)
                if callable(attr_val) and attr_name in method_names:
                    return timeit_decorator(attr_val)
                return attr_val

        return NewClassWrapper

    return class_decorator


@add_decorator_to_method_decorator("do_something1", "do_something2")
class TestModule(object):
    def __init__(self):
        pass

    def do_something1(self):
        print("do something1")

    def do_something2(self):
        print("do something2")


test_instance1 = TestModule()
test_instance1.do_something1()
test_instance1.do_something2()
# 输出：
#
# 将修饰器定义为类
# 随着项目变得更加复杂，我们有越来越多各种不同功能的修饰器需要维护，此时将修饰器简单的放在一个文件将会显得很混乱。此时我们可以按照功能，将修饰器封装到类中。当其他模块需要使用时，只需要import相应的类，即可方便的导入我们需要用到的修饰器。

# （1）不带参数的修饰器


class App(object):
    def route_decorator(self, func):
        def wrapper(*args, **kwargs):
            resp = func(*args, **kwargs)
            print(' '.join(['after', 'decorated']))
            return resp

        return wrapper


##其他模块只需要import修饰器类，即可使用
app = App()


@app.route_decorator
def test_01(device_id, *args, **kwargs):
    return ' '.join([device_id, str(args), str(kwargs)])


print(test_01("PH-NIO-001"))
# 输出如下
#
# 带额外参数的修饰器

import time
class App(object):
    def advance_decorator(self, loglevel="info"):
        print(' '.join(["log level is: ", str(loglevel)]))
        if loglevel == "debug":
            def decorator(func):
                def wrapper(*args, **kwargs):
                    st_time = time.time()
                    resp = func(*args, **kwargs)
                    end_time = time.time()
                    print(" ".join(["cost is: ", str(end_time - st_time)]))
                    return resp

                return wrapper
        else:
            def decorator(func):
                def wrapper(*args, **kwargs):
                    print("For your func test")
                    resp = func(*args, **kwargs)
                    return resp

                return wrapper
        return decorator


app = App()


@app.advance_decorator(loglevel="info")
def test_02(device_id, *args, **kwargs):
    return ' '.join([device_id, str(args), str(kwargs)])


print(test_02("PH-NIO-001"))
# 输出：
#
# 带可选参数的修饰器


def meter_collector(func=None, arg_index=None):
    def actual_decorator(func):
        @wraps(func)
        def __meter(self, *args, **kwargs):
            if arg_index:
                print(args)
                arg_tag = args[arg_index - 1]
                print(arg_tag)

            resp = func(self, *args, **kwargs)
            return resp

        return __meter

    if not func:
        def wait_func(func):
            return actual_decorator(func)

        return wait_func

    else:
        return actual_decorator(func)


class Demo(object):
    def __init(self):
        pass

    @meter_collector(arg_index=1)
    def test_func(self, device_id, data="python"):
        return (device_id + str(data))

    @meter_collector
    def test_func2(self, device_id, data="python2"):
        return (device_id + str(data))


demo = Demo()
data = demo.test_func("test")
print(data)

data2 = demo.test_func2("test")
print(data2)
# 执行结果：
# ('test',)
# test
# testpython
# testpython
# 8, 给多个类添加相同的类修饰器
# 当我们的项目中同时存在一批类或者子类需要添加修饰器时，我们可以选择给这些类分别加上修饰器。

from functools import wraps
import time
import random


def wait_random(min_wait=1, max_wait=30):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            time.sleep(random.randint(min_wait, max_wait))
            resp = func(self, *args, **kwargs)
            return resp

        return wrapper

    return decorator


def class_wrapper(cls):
    attrs = vars(cls)  ##等同于cls.__dict__
    for name, val in attrs.items():
        if callable(val):
            setattr(cls, name, wait_random(min_wait=1, max_wait=2)(val))
    return cls


@class_wrapper
class Scraper1(object):
    def func_to_scrape_1(self):
        print("func_to_scrape_1")
        # some scraping stuff


@class_wrapper
class Scraper2(object):
    def func_to_scrape_2(self):
        print("func_to_scrape_2")
        # some scraping stuff


Scraper1().func_to_scrape_1()
Scraper2().func_to_scrape_2()
# 同样的，在这种场景下我们有更好的选择 - -元类。
# ————————————————
# 版权声明：本文为CSDN博主「达西布鲁斯」的原创文章，遵循CC
# 4.0
# BY - SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https: // blog.csdn.net / biheyu828 / article / details / 82532126