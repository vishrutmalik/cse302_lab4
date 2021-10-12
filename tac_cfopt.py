import json 
import sys
import argparse
from cfg import *


def get_labels(body):
    labels = set()
    for instr in body:
        if instr["opcode"] == "label":
            labels.add(instr["args"][0])

    return labels

def new_label(labels, label_counter):
    while f"%.L{label_counter}" in labels:
        label_counter += 1
    return (f"%.L{label_counter}", label_counter)

def add_labels_jumps(proc):
    assert proc["proc"][0] == '@'
    body = proc["body"]
    labels = get_labels(body)
    label_counter = len(labels) #Could be 0 but this might save time
    if body[0]["opcode"] != "label":
        new_lbl, label_counter = new_label(labels, label_counter)
        labels.add(new_lbl)
        body.insert(0, {"opcode":"label", "args":[new_lbl], "result":None})

    labels_added = 0
    init_length = len(body)
    for i in range(1, init_length):
        j = i + labels_added
        if body[j]["opcode"][0] == 'j':
            if i == init_length - 1 or body[j+1]["opcode"] != "label":
                new_lbl, label_counter = new_label(labels, label_counter)
                labels.add(new_lbl)
                new_instr = {"opcode":"label", "args":[new_lbl], "result":None}
                body.insert(j + 1, new_instr)

    if "args" in proc.keys():
        return {"proc":proc["proc"], "args":proc["args"], "body":body}
    else:
        return {"proc":proc["proc"], "body":body}

def proc_to_blocks(proc):
    blocks = []
    body = proc["body"]
    current_block = []
    for instr in body:
        if instr["opcode"][0] == 'j' or instr["opcode"] == "ret":
            current_block.append(instr)
            blocks.append(current_block.copy())
            current_block = []
        elif instr["opcode"] == "label":
            if current_block != []:
                blocks.append(current_block.copy())
            current_block = [instr]
        else:
            current_block.append(instr)

    return blocks

def add_jumps(blocks):
    init_len=len(blocks)
    for i in range(init_len-1):
        if blocks[i][-1]["opcode"]!='jmp' and blocks[i][-1]["opcode"]!='ret':
            new_lbl= blocks[i+1][0]["args"][0]
            blocks[i].append({"opcode":"jmp", "args":[new_lbl], "result":None})
    return blocks



def main(fname, sname, coal, uce, jp1, jp2):
    with open(fname, 'r') as f:
        js_obj = json.load(f)

    for proc in js_obj:
        new_proc = add_labels_jumps(proc)
        blocks = proc_to_blocks(proc)
        blocks=add_jumps(blocks)
        for block in blocks:
            print(block)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    parser.add_argument("-o")
    parser.add_argument("--disable-coal", action="store_true", required=False)
    parser.add_argument("--disable-uce", action="store_true", required=False)
    parser.add_argument("--disable-jp1", action="store_true", required=False)
    parser.add_argument("--disable-jp2", action="store_true", required=False)
    args = parser.parse_args()

    main(args.fname, args.o, args.disable_coal, args.disable_uce,
         args.disable_jp1, args.disable_jp2)
