import json
import sys
import argparse
from cfg import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    parser.add_argument("-o")
    parser.add_argument("--disable-coal", action="store_true", required=False)
    parser.add_argument("--disable-uce", action="store_true", required=False)
    parser.add_argument("--disable-jp1", action="store_true", required=False)
    parser.add_argument("--disable-jp2", action="store_true", required=False)
    args = parser.parse_args()
    print(args)
