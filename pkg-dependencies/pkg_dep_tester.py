import os
import sys
import subprocess
from model_test import test_model_usage

root = os.path.abspath (os.path.join(os.path.split(__file__)[0], '..' ) )
if root not in sys.path: sys.path.append(root)


def run_model_test(file_name):
    sysout, syserr = sys.stdout, sys.stderr

    errfile = f'{file_name}_err.txt'
    outfile = f'{file_name}_out.txt'

    with open(outfile, 'w') as out:
        with open(errfile, 'w') as err:
            # route output to that location
            sys.stdout = out
            sys.stderr = err

            # call the model
            rc = test_model_usage()

    # restore stdout 
    sys.stdout = sysout
    sys.stderr = syserr
    return outfile, errfile, rc

def main():
    outputdir = os.path.join(root, 'pkg-dependencies', 'testoutputs')

    print('Run')
    _ ,_ , rc = run_model_test(os.path.join(outputdir, 'sample'))
    print('Done: ', rc)
    return 0

if __name__ == '__main__':
    sys.exit(main())