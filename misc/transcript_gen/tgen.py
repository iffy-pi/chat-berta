import sys
import traceback
import time
import json
import os
import requests
import math

def pprint(e):
    print(json.dumps(e, indent=4))

def round_to_multiple(number, multiple):
    while (number % multiple != 0):
        number += 1
    return number

def get_output_lines(lines, linecnt, count):
    line_grps = int ( count / linecnt )
    rem_lines = count % linecnt
    rem_lines = round_to_multiple(rem_lines, 3) +2

    outline = []
    for _ in range(line_grps):
        outline += lines[:-1] + ['{}\n'.format(lines[-1].strip()), '\n' ]

    outline += lines[:rem_lines-1] + [ lines[rem_lines-1].strip() ]

    return outline


def main():

    count = int(sys.argv[1])

    file_dir = os.path.split ( os.path.abspath( __file__))[0]
    root_dir = os.path.abspath ( os.path.join(file_dir, '..', '..'))
    r4 = os.path.join(root_dir, 'apiutils', 'samples', 'sample_raw_chat_4.txt')

    with open(r4, 'r') as file:
        lines = file.readlines()

    linecnt = len(lines)

    output_file = os.path.join( file_dir, 'out.txt')
    output_lines = get_output_lines(lines, linecnt, count)

    # write to file
    with open(output_file, 'w') as file:
        file.writelines(output_lines)

    return 0
 

if __name__ == "__main__":
    sys.exit(main())
