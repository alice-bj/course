# -*- coding:utf-8 -*-
import os
import pickle


class Mypickle:
    def __init__(self,pathname):
        self.pathname = pathname

    def dump(self,data):
        with open(self.pathname,'ab') as f:
            pickle.dump(data,f)

    def load(self):
        if os.path.isfile(self.pathname):
            with open(self.pathname,'rb') as f:
                while True:
                    try:
                        data = pickle.load(f)
                        yield data
                    except Exception as e:
                        break

    def edit(self,data):
        f_temp = Mypickle(self.pathname+'.bak')
        with open(self.pathname,'rb+') as f:
            for i in self.load():
                if i.name == data.name:
                    f_temp.dump(data)
                else:
                    f_temp.dump(i)
        os.replace(f_temp.pathname,f.name)