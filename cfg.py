import sys

class Node:
    def __init__(self,label,body=None):
        self.label=label
        self.instrs= body if body is not None else []
        self.jumps=[]
        self.jumps=self.get_dest()

    def last_instr(self):
        return self.instrs[-1]
    
    def get_dest(self):
        for instr in self.instrs:
            if instr["opcode"][0]=='j' and instr["args"][-1] not in self.jumps:
                self.jumps.append(instr["args"][-1])
        return self.jumps

class CFG:
    def __init__(self,proc,nodes):
        self.proc= proc
        self.nodes=nodes
        self.edges=[]
        




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




