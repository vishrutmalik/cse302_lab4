import json
import sys
import argparse
from cfg import *


def get_labels(body):
    labels = set()
    for instr in body:
        if instr["opcode"] == "label":
            assert instr["args"][0][:1] == "%."
            labels.add(instr["args"][0])

    return labels

def new_label(labels, label_counter):
    while f"%.L{label_counter}" in labels:
        label_counter += 1
    return (f"%.L{label_counter}", label_counter)

def add_labels_jumps(proc):
    assert proc["proc"][0] == '@'
    assert proc["body"][0]["args"][0] == '@'
    body = proc["body"]
    labels = get_labels(body)
    label_counter = len(labels) #Could be 0 but this might save time
    if body[1]["opcode"] != "label":
        new_lbl, label_counter = new_label(labels, label_counter)
        body.insert({"opcode":"label", "args":[new_lbl], "result":None})


def main(fname, sname, coal, uce, jp1, jp2):
    with open(fname, 'r') as f:
        js_obj = f.read()

    for proc in js_obj:
        add_labels_jumps(proc)

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
