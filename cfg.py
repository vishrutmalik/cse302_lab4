import sys

class Node:
    def __init__(self,label,body=None):
        self.label=label
        self.instrs= body if body is not None else []
        self.jumps=[]
        self.get_dest()

    def last_instr(self):
        return self.instrs[-1]
    
    def get_dest(self):
        self.jumps=[]
        for instr in self.instrs:
            if instr["opcode"][0]=='j' and instr["args"][-1] not in self.jumps:
                self.jumps.append(instr["args"][-1])


class CFG:
    def __init__(self,proc,nodes):
        self.proc= proc
        self.nodes=nodes
        self.nodes_to_labels = {node:node.label for node in self.nodes}
        self.labels_to_nodes = {node.label:node for node in self.nodes}
        self.entry = self.nodes[0]
        self.edges=dict()
        self.update_edges()


    def update_edges(self):
        self.edges=dict()
        for node in self.nodes:
            self.edges[node.label]=node.jumps

    def next(self, node):
        return self.edges[node.label]

    def prev(self, node):   
        prevs=[]
        for lab in self.edges.keys():
            if node.label in self.edges[lab]:
                prevs.append(lab)
        return prevs

    def new_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
            self.update_edges()

    def delete_node(self, node):
        if node in self.nodes:
            for dest in self.edges[node.label]:
                self.remove_edge(node.label,dest)
            self.nodes.remove(node)
    
    def remove_edge(self,src,dest):
        if dest in self.edges[src]:
            self.edges[src].remove(dest)

    def add_edge(self,src,dest):
        if dest not in self.edges[src]:
            self.edges[src].append(dest)
    
    def aux_uce(self, node, visited):
        visited.add(node)
        for nbr_label in self.next(node):
            neighbour = self.labels_to_nodes[nbr_label]
            if neighbour not in visited:
                self.aux_uce(neighbour, visited)

    def uce(self):
        visited = set()
        self.aux_uce(self.entry, visited)
        for node in self.nodes:
            if node not in visited:
                self.delete_node(node)
        self.update_edges()
