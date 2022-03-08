# #
# # # a = set()
# # # a.add("111")
# # # a.add("1111")
# # # print(list(a))
# # #
# # # print(len([]))
# #
# #
# # class A:
# #     def add(self, x):
# #         y = x + 1
# #         print(y)
# #
# #
# # class B(A):
# #     def add(self, c):
# #         super().add(c)
# #
# #
# # class FooParent(object):
# #     def __init__(self):
# #         self.parent = 'I\'m the parent.'
# #         print('Parent')
# #
# #     def bar(self, message):
# #         print("%s from Parent" % message)
# #
# #
# # class FooChild(FooParent):
# #     def __init__(self):
# #         # super(FooChild,self) 首先找到 FooChild 的父类（就是类 FooParent），然后把类 FooChild 的对象转换为类 FooParent 的对象
# #         super(FooChild, self).__init__()
# #         # print('Child')
# #
# #     def bar(self, message):
# #         super(FooChild, self).bar(message)
# #         print('Child bar fuction')
# #         print(self.parent)
# #
# #
# # if __name__ == '__main__':
# #     fooChild = FooChild()
# #     fooChild.bar('HelloWorld')
# #
# #
# # a = False
# # b = False
# # if a is False and b is False:
# #     print(1)
# # elif a is False and b is True:
# #     print(2)
# # elif a is True and b is False:
# #     print(3)
# # else:
# #     print(4)
#
# for phone in [0, 1]:
#     page = 1
#     # print(phone)
#     # 查询企业是否转移到机器人
#     resp_robot_com=[{'per_page': 1000}, {'per_page': 2}]
#     for i in range(1, page+1):
#         print(phone)
#         print(page)
#         if not resp_robot_com:  # 判断转移的企业在机器人内是否存在
#             if phone == 0:
#                 resp_robot_verdicts_mobile = False
#             else:
#                 resp_robot_verdicts_fixed = False
#         else:
#             for j in resp_robot_com:
#                 if j['per_page'] == 1000:
#                     page += 1
#                     print(page)
#
class A:
    def __init__(self, x, y, ):
        # super(A, self).__init__(*args)
        self.x = x
        self.y = y
        print("In class A's init...")

    def Aprint(self):
        print("AAAAAAAAAAAAA")

class C:
    def __init__(self, l=1, n=2):
        # super(C, self).__init__(*args)
        self.s = l
        self.d = n
        print("In class A's init...")

    def Aprit(self):
        print("sssssss")


class B(A):
    def __init__(self, z, K, x, y):
        # super(A).__init__() # 覆盖A的初始化参数
        # super().__init__(x, y) # 继承A的初始化参数 == super(B, self).__init__(x, y)
        # super().__init__()
        # super(B, self).__init__(z, K, x, y, l, n)
        # super(B, self).__init__(z, K)
        super(B, self).__init__(x, y)
        # super(C, self).__init__(l, n)

        self.z = z
        self.k = K
        print("In class B's init...")

    def Bprint(self):
        print("BBBBBBBBBBBBB")


demo = B(z=1,K=2,x=3,y=4)
print(demo.z)
print(demo.x)
print(demo.y)
# print(demo.s)
# print(demo.d)
print(demo.k)
demo.Aprint()
demo.Bprint()
# demo.Aprit()
