# 对于子类继承父类的变量，要显示的定义和赋初值，否则会出现混乱，如下
class AA(object):
    c_var = 1  # 类变量

    def __init__(self, var):
        self.object_var = var  # 实例变量


class BB(AA):
    pass


class CC(AA):
    pass


if __name__ == '__main__':
    BB.c_var = 2
    print(AA.c_var)  # 1
    print(BB.c_var)  # 2
    print(CC.c_var)  # 1
    AA.c_var = 3
    print(AA.c_var)  # 3
    print(BB.c_var)  # 2
    print(CC.c_var)  # 3

    print(AA.__dict__)
    # {'__module__': '__main__', 'x': 3, '__init__': <function AA.__init__ at 0x000001B478ACB8C8>,
    # '__dict__': <attribute '__dict__' of 'AA' objects>,
    # '__weakref__': <attribute '__weakref__' of 'AA' objects>, '__doc__': None}
    aa = AA(5)
    print(aa.__dict__)  # {'object_var': 5}
    # 在对象的命名空间中找
    print(aa.object_var)  # 5
    # 在对象的命名空间中找不到class_var，则从类的命名空间中寻找
    print(aa.c_var)  # 3
