

from pygame import init


class Updater():

    def __init__(self) -> None:
        self.arr=[]
        pass

    def add(self,obj):
        self.arr.append(obj)

    def update(self):
        for i in self.arr:
            i.setState()
            i.update()
            i.show()
