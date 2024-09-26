
def bubbling_sort(info_list):
    # 冒泡排序
    n = len(info_list)
    for i in range(n-1):
        for j in range(n-1-i):
            if info_list[j] > info_list[j+1]:
                info_list[j], info_list[j+1] = info_list[j+1], info_list[j]
    print(info_list)
a = [5, 1, 9, 8, 3, 11, 15, 12]
bubbling_sort(a)


def select_sort(info_list):
    # 选择排序
    n = len(info_list)
    for i in range(n):
        max_index = i
        for j in range(i+1, n):
            if info_list[max_index] < info_list[j]:
                max_index = j
        info_list[i], info_list[max_index] = info_list[max_index], info_list[i]
    print(info_list)
# select_sort(a)

def insert_sort(info_list):
    # 插入排序
    n = len(info_list)
    for i in range(1, n):
        one = info_list[i]
        j = i -1
        while j >= 0 and one > info_list[j]:
            info_list[j+1] = info_list[j]
            j -= 1
        info_list[j+1] = one
    print(info_list)

# insert_sort(a)

def quickly_sort(info_list, start, end):
    if start > end:
        return
    mid = info_list[start]
    low = start
    higth = end
    while low < higth:
        while low < higth and info_list[higth] > mid:
            higth -= 1
        info_list[low] = info_list[higth]
        while low < higth and info_list[low] <= mid:
            low += 1
        info_list[higth] = info_list[low]
    info_list[low] = mid
    quickly_sort(info_list, start, low-1)
    quickly_sort(info_list, low+1, end)
# quickly_sort(a, 0, len(a)-1)


def merge_sort(arr):
    # 归并排序
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    return merge(left_half, right_half)

def merge(left, right):
    result = []
    left_idx = right_idx = 0
    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] < right[right_idx]:
            result.append(left[left_idx])
            left_idx += 1
        else:
            result.append(right[right_idx])
            right_idx += 1

    result.extend(left[left_idx:])
    result.extend(right[right_idx:])

    return result

def binarySearch(arr, l, r, x):
    # 基本判断
    if r >= l:
        mid = (l+r)//2 # 元素整好的中间位置
        if arr[mid] == x:
            return mid
        # 元素小于中间位置的元素，只需要再比较左边的元素
        elif arr[mid] > x:
            return binarySearch(arr, l, mid-1, x)
        # 元素大于中间位置的元素，只需要再比较右边的元素
        else:
            return binarySearch(arr, mid+1, r, x)
    else: # 不存在
        return -1


def binar_list(arr, l, r, x):
    if r - l >= 0:
        mid = (l+r)//2
        if arr[mid][0] <= x <= arr[mid][-1]:
            return mid
        elif arr[mid][-1] < x:
            return binar_list(arr, mid+1, r, x)
        else:
            return binar_list(arr, l, mid-1, x)
    else:
        return -1



def get_one_num(one_info_list, one_num):
    row_index = binar_list(a_list, 0, len(a_list)-1, one_num)
    if row_index < 0:
        return '不在数组中'
    col_index = binarySearch(one_info_list[row_index], 0, len(one_info_list[row_index])-1, one_num)
    if col_index < 0:
        return '不在数组中'
    else:
        return row_index, col_index

# a_list = [[1, 2, 3, 4,], [5, 6, 7, 8, 9], [10, 11, 12, 13], [15, 16, 17, 18], [19, 20]]
a_list = [[1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13]]
res = get_one_num(a_list, 13)
print('数组中的位置为：', res)

print()
# 实现单利模式
class Single(object):
    _instance = None
    def __init__(self, *args, **kwargs):
        self.args = args
        print(self.args)
        self.kwargs = kwargs

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

a = Single('888')
print(id(a))
b = Single('666')
print(id(b))


# 用函数实现装饰器
from functools import wraps

def decorator(cls):
    instance = {}
    @wraps(cls)
    def wrapTheClass(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
            print('A new instance!')
        else:
            print('No more instance!')
        return instance[cls]
    return wrapTheClass


@decorator
class myclass(object):
    instanceNum = 0

    def __init__(self):
        myclass.instanceNum = myclass.instanceNum+1
    def getInstNum(self):
        return myclass.instanceNum

# 带参数的装饰器,
class A:
    def __init__(self, username):
        self.username = username
    def __call__(self, func):
        def inner(*args, **kwargs):
            print("this is call>>")
            result = func(*args, **kwargs)
            return result
        return inner

# a = A(usernaem="root"), func1 = a(func1)
@A(username="root")
def func1():
    time.sleep(1)
    print(" i am func1")

class Singleton:
    _instance = None

    def __init__(self, cls):
        self._wrapped = cls

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self._wrapped(*args, **kwargs)
        return self._instance

# 使用Singleton装饰器
@Singleton
class MySingleton:
    def __init__(self):
        pass

# 创建MySingleton的实例
obj1 = MySingleton()
obj2 = MySingleton()

# 验证obj1和obj2是否相同
print(obj1 is obj2)  # 输出: True


class MyError(Exception):
    # 自定义异常
    def __init__(self, msg):
        self.msg = msg



# 输入[1, 4], [1, 5], [7, 9], [9, 11]; 输出:[1, 5], [7, 11]

info_list = [[1, 4], [1, 5], [7, 9], [9, 11], [12, 0], [8, 12]]
def merge_range(info_list):
    info_list = [one_list for one_list in info_list if one_list[0] <= one_list[1]]
    info_sotred = sorted(info_list, key=lambda x:x[0])
    print(info_sotred)
    all_node_list = [info_sotred[0]]
    for one_info in info_sotred[1:]:
        if one_info[0] <= all_node_list[-1][-1]:
            if all_node_list[-1][-1] < one_info[-1]:
                all_node_list[-1][-1] = one_info[-1]
        else:
            all_node_list.append(one_info)
    for one in all_node_list:
        print(one)

merge_range(info_list)








# 基本类装饰器 ,那么用类来实现也是也可以的。我们可以让类的构造函数__init__()接受一个函数，
# 然后重载__call__()并返回一个函数，也可以达到装饰器函数的效果
class logging(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("[DEBUG]: enter function {func}()".format(
            func=self.func.__name__))
        return self.func(*args, **kwargs)
@logging
def say(something):
    print("say {}!".format(something))

# 带参数的类装饰器 , 如果需要通过类形式实现带参数的装饰器，那么会比前面的例子稍微复杂一点。那么在构造函数里接受的就不是一个函数，而是传入的参数。
# 通过类把这些参数保存起来。然后在重载__call__方法是就需要接受一个函数并返回一个函数。

class logging(object):
    def __init__(self, level='INFO'):
        self.level = level

    def __call__(self, func): # 接受函数
        def wrapper(*args, **kwargs):
            print("[{level}]: enter function {func}()".format(
                level=self.level,
                func=func.__name__))
            func(*args, **kwargs)
        return wrapper  #返回函数

@logging(level='INFO')# 先执行loggin(level='INFO'),再执行@
def say(something):
    print("say {}!".format(something))



def isValid(s):
    # 如果字符串长度为奇数，直接返回False
    if len(s) % 2 == 1:
        return False

    # 创建字典
    dct = {")": "(", "]": "[", "}": "{"}
    stack = list()   # 初始化栈stack（为列表）
    for char in s:    # 遍历字符串
        if char in dct:   # 如果遍历到的括号在字典中

            # 判断stack列表是否为空或最后一位是否为同类型右括号
            if not stack or stack[-1] != dct[char]:
                return False  # 不是则返回False
            stack.pop()  # 是则将其拿出匹配（删除）
        else:  # 如果遍历到的括号不在字典中，则将其添加到stack栈（列表）中
            stack.append(char)

    return not stack  # 若两两配对完成，则栈（列表）被取空

info_str = '{[}]'
print(isValid(info_str))

