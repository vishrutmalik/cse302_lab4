import sys
import json
import argparse
import tac2x64
import bx2tac
import tac_cfopt

def main(filename, keep_tac, stop_tac):
    if filename.endswith(".tac.json"):
        asm = tac2x64.tac_to_asm_f(filename)
        tac2x64.compile_tac(asm, filename)

    elif filename.endswith(".bx"):
        rname = filename[:-3] + ".tac.json"
        tac = bx2tac.to_tac(filename, False)
        tac = tac_cfopt.main(tac)

        if keep_tac:
            with open(rname, 'w') as afp:
                json.dump(tac, afp, indent=1)
            print(f"{rname} produced")

        if not stop_tac:
            asm = tac2x64.tac_to_asm(tac)
            tac2x64.compile_tac(asm, filename)

    else:
        print("Filename does not end with .bx or .tac.json")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--keep-tac", action="store_true", required=False)
    parser.add_argument("--stop-tac", action="store_true", required=False)
    args = parser.parse_args()

    main(args.filename, args.keep_tac, args.stop_tac)
