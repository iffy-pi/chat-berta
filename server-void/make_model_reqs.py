import sys
import os
import subprocess

# Packages in the model requirements list that could not be installed
PKG_BLACKLIST = [
    # Commented ones are ones that can be installed but not with the specified version (See NOVERS_INSTALL)
    'bzip2',
    'c-ares',
    'ca-certificates',
    'conda',
    'conda-content-trust',
    'conda-package-handling',
    'conda-package-streaming',
    'console_shortcut_miniconda',
    
    # 'grpcio',
    # 'intel-openmp',

    'libabseil',
    'libblas',
    'libcblas',
    'libffi',
    'libgrpc',
    'libhwloc',
    'libiconv',
    'liblapack',
    'libprotobuf',
    'libsqlite',
    'libxml2',
    'libzlib',
    'menuinst',
    'openssl',

    'pip',
    'powershell_shortcut_miniconda',
    'pthreads-win32',

    # 'pycosat',
    
    'python',
    'python_abi',
    're2',

    # 'tbb',
    # 'tk',
    # 'torch',
    # 'torchaudio',
    # 'torchvision',

    'ucrt',

    # 'vc',

    'vs2015_runtime',
    'xz',
    'zlib'
]

# Packages that can be installed but without a version
NOVERS_INSTALL = [
    'grpcio',
    'intel-openmp',
    'pycosat',
    'tbb',
    'tk',
    'torch',
    'torchaudio',
    'torchvision',
    'vc'
]

# Packages in blacklist that we want to install but cant as they cannot be found in pip
STILL_NOT_WORKING = [
    # Commented ones are packages that we do not need to install e.g. conda stuff
    'bzip2',
    'c-ares',
    'ca-certificates',
    # 'conda',
    # 'conda-content-trust',
    # 'conda-package-handling',
    # 'conda-package-streaming',
    # 'console_shortcut_miniconda',
    'libabseil',
    'libblas',
    'libcblas',
    'libffi',
    'libgrpc',
    'libhwloc',
    'libiconv',
    'liblapack',
    'libprotobuf',
    'libsqlite',
    'libxml2',
    'libzlib',
    'menuinst',
    'openssl',
    # 'pip',
    # 'powershell_shortcut_miniconda',
    'pthreads-win32',
    # 'python',
    # 'python_abi',
    're2',
    'ucrt',
    # 'vs2015_runtime',
    'xz',
    'zlib'
]


def install_package(name, ver=None):

    arg = '{}{}'.format( name, f'=={ver}' if ver is not None else '')
    child = subprocess.Popen(['pip', 'install', arg])
    child.communicate()

def load_model_reqs():
    # loads the model requirements and returns a list dictionaries in the format of { name: <package name>, 'ver': <version> , 'other':}

    packages = []

    with open ( os.path.join( os.path.abspath(os.path.split(__file__)[0]), 'apiutils', 'model', 'requirements.txt') , 'r') as file:
        lines = file.readlines()
        for l in lines:
            l = l.strip()
            
            if l.startswith('#'): continue

            if len(w := l.strip().split('=')) == 3:
                packages.append({
                    'name': w[0],
                    'ver': w[1],
                    'other': w[2]
                })


    return packages

def install_model_pkgs():
    pkgs = load_model_reqs()

    for p in pkgs:
        if p['name'] in PKG_BLACKLIST: continue
        ver = p['ver']
        if p['name'] in NOVERS_INSTALL: ver = None

        print('============================================================================================')
        print('Installing: {}'.format(p['name']))
        install_package( p['name'], ver=ver)
        print('============================================================================================')

def custom_install( pkgnames ):
    pkgs = load_model_reqs()

    for p in pkgs:
        if p['name'] not in pkgnames: continue
        print('============================================================================================')
        print('Installing: {}'.format(p['name']))
        install_package( p['name'])
        print('============================================================================================')


def test():
    with open(os.path.join( os.path.abspath(os.path.split(__file__)[0]), 'model_info.txt') , 'r') as file:
        lines = file.readlines()
        for l in lines:
            l = l.strip()
            if not l.startswith('Installing: '): continue
            print(l.replace('Installing: ', ''))

def main():
    # install_model_pkgs()
    custom_install( STILL_NOT_WORKING )
    
    return 0

if __name__ == '__main__':
    sys.exit(main())