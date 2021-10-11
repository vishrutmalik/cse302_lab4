import sys


class cfg:
    def __init__(self, js_obj):
        self.obj=js_obj
        self.edges={}
        pass

    def new_node(self):
        pass


class Node(cfg):
    def __init__(self, pred, succ):
        self.pred= None; #as of now
        self.succ= None; #as of now
        pass
    
    def next(self):
        return self.succ

    def prev(self):
        return self.pred


