import argparse
import json

def parse_body(line):
    nb_brackets = 0
    line = line.strip()

    res = []
    current_string = ""
    current_list = []
    for i, c in enumerate(line):
        if c == '[':
            nb_brackets += 1
        elif c == ']':
            nb_brackets -= 1
            if current_string != "":
                current_list.append(current_string)
                current_string = ""
            res.append(current_list.copy())
            current_list = []
        elif c == ' ' and nb_brackets == 0:
            if current_string != "":
                res.append(current_string)
                current_string = ""
        elif c == ' ' and nb_brackets > 0:
            if current_string != "":
                current_list.append(current_string)
                current_string = ""
        else:
            current_string += c

    res.append(current_string)
    return res

def main(fname):
    with open(fname, 'r') as f:
        to_parse = f.read()

    lines = to_parse.splitlines()
    body = []
    for line in lines:
        line.strip()
        parsed = parse_body(line)
        assert len(parsed) == 3
        assert isinstance(parsed[1], list)
        temp = {}
        temp["opcode"] = parsed[0]
        temp["args"] = parsed[1]
        temp["result"] = parsed[2]
        body.append(temp)

    res = {"proc": "@main",
           "args": [],
           "body": body}

    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    parser.add_argument("--create-json", action="store_true", required=False)
    parser.add_argument("--print", action="store_true", required=False)

    args = parser.parse_args()

    res = main(args.fname)
    if args.print:
        print(res)

    if args.create_json:
        if args.fname[-4:] == ".ssv":
            jname = args.fname[:-4] + ".tac.json"
        elif '.' in args.fname:
            i = args.fname.find(".")
            jname = args.fname[:i] + ".tac.json"
        else:
            jname = args.fname + ".tac.json"

        with open(jname, 'w') as f:
            json.dump(res, f, indent=4)
