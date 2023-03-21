import os
import sys
import subprocess
from model_test import test_model_usage
import json

SCRIPTDIR = os.path.abspath ( os.path.split(__file__)[0] )
root = os.path.abspath (os.path.join(os.path.split(__file__)[0], '..' ) )
if root not in sys.path: sys.path.append(root)

REQS_BEFORE_MODEL_FILE = os.path.join( root, 'docs', 'misc', 'requirements_before_model.txt' )
CUR_REQS_FILE = os.path.join(root, 'requirements.txt')

def pprint(obj):
    print(json.dumps(obj, indent=4))

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


def parse_pip_reqs(filename):
    # returns dictionary of pip requirements
    # loads the model requirements and returns a list dictionaries in the format of { name: <package name>, 'ver': <version> , 'other':}

    packages = {}

    with open ( filename , 'r') as file:
        lines = file.readlines()
        for l in lines:
            l = l.strip()
            
            if l.startswith('#'): continue

            if len(w := l.strip().split('==')) == 2:

                if w[0] in packages.keys():
                    raise Exception('Duplicate package!')
                
                packages[w[0]] = {
                    'name': w[0],
                    'ver': w[1],
                    'other': ''
                }


    return packages

def install_package(name, ver=None):

    arg = '{}{}'.format( name, f'=={ver}' if ver is not None else '')
    child = subprocess.Popen(['pip', 'install', arg])
    child.communicate()

def uninstall_package(name):
    arg = name
    child = subprocess.Popen(['pip', 'uninstall', arg, '-y'])
    child.communicate()





def main():
    outputdir = os.path.join(root, 'pkg-dependencies', 'testoutputs')

    reqs_before_model = parse_pip_reqs(REQS_BEFORE_MODEL_FILE)
    cur_reqs = parse_pip_reqs(CUR_REQS_FILE)

    # get packages that were added because of the model
    bmk = reqs_before_model.keys()
    ck = cur_reqs.keys()
    new_pkgs = list(filter(
        lambda pkg: pkg not in bmk, # add the package if it wasnt used before
        ck
    ))

    pkgs_to_keep = []
    pkgs_to_discard = []

    for pkg in new_pkgs:
        print('=====================================================================')
        print(f'Testing: {pkg}')
        # will be doing some AB testing
        cur_output = os.path.join(outputdir, pkg)

        # uninstall the package
        print(f'Uninstalling "{pkg}"...')
        print('===========>')
        uninstall_package(pkg)
        print('===========>')

        # do the model test
        print('\nRunning model test')
        print('===========>')
        out, err, rc = run_model_test(cur_output)
        print(f'Model Result: {rc}')
        print('===========>')
        print('')
        if rc != 0:
            # if return code is not 0, then this package is dependent
            # we should keep the package

            print(f'"{pkg}" is needed!')
            pkgs_to_keep.append(pkg)
            # install the package again
            print('Resinstalling...')
            print('===========>')
            install_package( pkg, ver=cur_reqs[pkg]['ver'] )
            print('===========>')

        else:
            print(f'"{pkg}" is NOT needed!')
            # not needed , so discard it
            pkgs_to_discard.append(pkg)

        print('=====================================================================')

        # save the list to file
        with open( os.path.join(SCRIPTDIR, 'results.txt'), 'w' ) as file:
            sysout  = sys.stdout
            sys.stdout = file

            print('Packages to keep: ')
            pprint(pkgs_to_keep)

            print('')
            print('Packages to discard: ')
            pprint(pkgs_to_discard)

            sys.stdout = sysout

        print('Testing Complete')

    return 0

if __name__ == '__main__':
    sys.exit(main())