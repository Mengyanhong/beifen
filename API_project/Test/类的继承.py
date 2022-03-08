# class A(object):
#     def __init__(self):
#         print('Running A.__init__')
#         super(A, self).__init__()
#
#
# class B(A):
#     def __init__(self):
#         print('Running B.__init__')
#         # super(B,self).__init__()
#         A.__init__(self)
#
#
# class C(A):
#     def __init__(self):
#         print('Running C.__init__')
#         super(C, self).__init__()
#
#
# class D(B, C):
#     def __init__(self):
#         print('Running D.__init__')
#         super(D, self).__init__()
#
#
# foo = D()

class AAA(object):
    def __init__(self, class_num):
        self.class_num = class_num
        print('AAA init ! ' + str(class_num))

    def talk_to_all(self):
        print("I am AAA!")


class A(AAA):
    def __init__(self, class_num, *args):
        super(A, self).__init__(*args)
        self.class_num = class_num
        print('A init ! ' + str(class_num))

    def talk_to_all(self):
        print("I am A!")


class B(AAA):
    def __init__(self, class_num, *args):
        super(B, self).__init__(*args)
        self.class_num = class_num
        print('B init ! ' + str(class_num))

    def talk_to_all(self):
        print("I am B!")


class C(A, B):
    def __init__(self, class_num, *args):
        super(C, self).__init__(*args)
        self.class_num = class_num
        print("C Init ! " + str(class_num))

    def talk_to_all(self):
        print("==== I am C! ====")
        super(B, self).talk_to_all()


if __name__ == '__main__':
    test = C(1, 2, 3, 4)
    test.talk_to_all()
    print(C.__mro__)