import sys

class Node:
    def __init__(self, pred, succ, body):
        self.label=None
        self.body=body
        self.pred= None; #as of now
        self.succ= None; #as of now
        pass
    
    def next(self):
        return self.succ

    def prev(self):
        return self.pred

    def instr(self):
        pass

class CFG:
    def __init__(self, js_obj, proc, label, nodes):
        self.obj=js_obj
        self.proc= proc
        self.label=label
        pass

    def new_node(self):
        pass

    def successor(self):
        pass

    def predecessor(self):
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

    


