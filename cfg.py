import sys

class Node:
    def __init__(self,label,body=None):
        self.label=label
        self.body= body if body is not None else []
        self.instrs= [instr for instr in body]

    def last_instr(self):
        return self.instrs[-1]
    


class CFG:
    def __init__(self,proc,label, nodes):
        self.label=label
        self.proc= None
        self.jumps=None
        self.instrs=[]
        pass



    def new_node(self):
        pass

    def next(self, node):
        pass

    def prev(self, node):   
        pass

    def edges(self):
        #create a list of tuples?
        pass

    def new_node(self):
        pass

    def delete_node(self):
        pass
    
    def remove_edge(self):
        pass

    def add_edge(self):
        pass




