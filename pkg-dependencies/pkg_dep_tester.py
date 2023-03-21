import os
import sys
import subprocess
import json

SCRIPTDIR = os.path.abspath ( os.path.split(__file__)[0] )
root = os.path.abspath (os.path.join(os.path.split(__file__)[0], '..' ) )
if root not in sys.path: sys.path.append(root)


VENV_PYTHON = os.path.join(root, 'venv', 'Scripts', 'python.exe')
MODEL_FILE = os.path.join(SCRIPTDIR, 'model_test.py')
REQS_BEFORE_MODEL_FILE = os.path.join( root, 'docs', 'misc', 'requirements_before_model.txt' )
CUR_REQS_FILE = os.path.join(root, 'requirements.txt')

def pprint(obj):
    print(json.dumps(obj, indent=4))


def run_model_test(file_name):
    # clear the caches
    apiutils = os.path.join(root, 'apiutils')
    # subprocess.Popen(['rd', '/q', '/s', r'C:\Users\omnic\local\GitRepos\chat-berta\apiutils\nec\__pycache__']).communicate()
    # subprocess.Popen(['rd', '/q', '/s', r'C:\Users\omnic\local\GitRepos\chat-berta\apiutils\model\__pycache__']).communicate()

    sysout, syserr = sys.stdout, sys.stderr

    errfile = f'{file_name}_err.txt'
    outfile = f'{file_name}_out.txt'

    with open(outfile, 'w') as out:
        with open(errfile, 'w') as err:
            # route output to that location
            sys.stdout = out
            sys.stderr = err

            child = subprocess.Popen([VENV_PYTHON, MODEL_FILE], stdout=out, stderr=err)
            child.communicate()
            # call the model
            rc = child.returncode

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

    known_needed_pkgs = [
        'spacy',
        'spacy-legacy',
        'spacy-loggers',
        'torch',
        'transformers',
        'aiohttp',
        'aiosignal',
        "async-timeout",
        "attrs",
        "blis"
    ]

    known_pkgs_to_discard = [
        'zstd',
        'pycosat',
        'sklearn',
        'absl-py',
        "absl-py",
        "asgiref",
        "blinker",
        "Brotli"
    ]

    # get packages that were added because of the model
    bmk = reqs_before_model.keys()
    ck = cur_reqs.keys()
    new_pkgs = list(filter(
        lambda pkg: pkg not in bmk,
        ck
    ))

    pkgs_to_keep = []
    pkgs_to_discard = []

    checkfile = os.path.join(outputdir, 'check')

    for pkg in new_pkgs:
        print('=====================================================================')
        print(f'Testing: {pkg}')
        # will be doing some AB testing
        cur_output = os.path.join(outputdir, pkg)

        reinstall = True
        
        known_keep = pkg in known_needed_pkgs
        known_discard = pkg in known_pkgs_to_discard

        if (known_keep or known_discard):
            if known_keep:
                print(f'Known Keep for {pkg}')
                rc = 1
                reinstall = False
            else:
                print(f'Known discard for {pkg}')
                rc = 0

        else:
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
            
            if reinstall:
                # install the package again
                print('Resinstalling...')
                print('===========>')
                install_package( pkg, ver=cur_reqs[pkg]['ver'] )
                print('===========>')

                # recheck model
                print(f'Checking reinstall for {pkg}')
                out, err, rc = run_model_test(checkfile)
                if rc != 0:
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
                    raise Exception(f'Model not working after package "{pkg}" reinstall! Results have been written to file!')
            

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