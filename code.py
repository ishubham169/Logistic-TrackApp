from dataclasses import dataclass
class a():
    def __init__(self,num):
        print("Class a",num)

class b(a):
    def __init__(self,num):
        print("Class b",num)
        A.__init__(self,num-1)

if True:
   obj = b(10)
print("hello")
print("shubham")

