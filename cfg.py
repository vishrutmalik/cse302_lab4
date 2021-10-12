import sys

class Node:
    def __init__(self,body):
        self.label=None
        self.body=body
        pass
    
    def next(self):
        return self.succ

    def prev(self):
        return self.pred

    def instr(self):
        pass

class CFG:
    def __init__(self,proc,label, nodes):
        self.label=label
        self.proc= None
        self.args=js_obj['args']
        self.jumps=None
        assert js_obj['proc'][0]=='@'
        self.instrs=[]
        pass

    def instrs(self):
        for instr in js_obj['body']:


    def new_node(self):
        pass

    def next(self, node):
        pass

    def prev(self, node):
        pass

    def edges(self):
        #create a tuples?
        pass

    def new_node(self):
        pass

    def delete_node(self):
        pass
    
    def remove_edge(self):
        pass

    def add_edge(self):
        pass




