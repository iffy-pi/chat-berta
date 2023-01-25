# simple python scripts that automatically makes our shared link files
import os
import sys

# this is the place we will be linking to
MASTER_SHARED_DIR = os.path.split(__name__)[0]
APP_SHARED_DIR = os.path.join( MASTER_SHARED_DIR, '..', 'src', 'shared-linked')
API_SHARED_DIR = os.path.join( MASTER_SHARED_DIR, '..', 'apiutils', 'shared-linked')

# shared_files.txt contains files in the shared-linked directory that should be shared
# File just consists of file names local to the shared-linked directory
# open the file and iterate through all the items

with open( os.path.join(MASTER_SHARED_DIR, 'shared_files.txt'), 'r') as file:
    shared_files = [ line.strip() for line in  file.readlines() ]

    for shared_file in shared_files:
        # make the hard link with os.link
        src_file_path = os.path.join(MASTER_SHARED_DIR, shared_file )
        for dest in [ APP_SHARED_DIR, API_SHARED_DIR ]:
            link_dest_path = os.path.join(dest, shared_file)
            # delete the file if it already exists at that location
            if os.path.exists( link_dest_path ):
                os.remove( link_dest_path )
                print('Deleted {}'.format(link_dest_path))

            os.link( src_file_path, link_dest_path  )
            print('Link Created: {} <===> {}'.format(src_file_path, link_dest_path))
