
class Mom:
    def __new__(cls):
        print('Mom__new__')
        return object().__new__(cls)

    def __init__(self):
        print('__init__')


class Son(Mom):
    def __new__(cls):
        print('Son__new__')
        # 如果没有返回值，则不会创建实例，init方法也不会调用
        # return super(Son, cls).__new__(cls)

    def __init__(self):
        print('__init__')
        # super(Mom, self).__init__()
if __name__ == '__main__':
  son = Son()
  mom = Mom()

>>>
Son__new__
Mom__new__
__init__
