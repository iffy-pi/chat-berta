import sys
import requests
import os
import mimetypes
import json

def prettify(d: dict) -> str:
    return json.dumps(d, indent=4)

class PushBulletFileServerException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class exceptions:
    class BadServerResponseError(PushBulletFileServerException):
        '''Thrown when PushBullet server response is not successful, returns information about the response if available'''
        def __init__(self, code, message=None):
            super().__init__('Code: {}{}'.format(code, ', Response: "{}"'.format(message) if message is not None else ''))


    class InvalidParameters(PushBulletFileServerException):
        '''Thrown when given method parameters are invalid or inadequate'''
        def __init__(self, msg):
            super().__init__(msg)

    class InvalidConfiguration(PushBulletFileServerException):
        '''Thrown when method encounters an error with the provided parametes'''
        def __init__(self, msg):
            super().__init__(msg)

    class UnreachableServerAddress(PushBulletFileServerException):
        '''Thrown when given server path is unreachable, i.e. outside address bounds'''
        def __init__(self, address):
            super().__init__(f'Provided address "{address}" is unreachable!')

    class InvalidServerAddress(PushBulletFileServerException):
        def __init__(self, address):
            super().__init__(f'Provided address "{address}" is invalid! Addresses must be absolute!')


class PushBulletFileServer():
    # simple file server using the pushbullet server as a save location
    PUSHBULLET_API = 'https://api.pushbullet.com/v2'
    __INDEX_PUSH_TITLE = 'PushBullet File Server File Index'
    VERSION = 1.0
    DEVICE_MANUFACTURER = 'PushBullet File Server'
    
    def __init__ (  self, access_token, 
                    index: dict=None,
                    server_name: str=None, # server, corresponds to device on pushbullet
                    server_iden: str=None, # identity of the server
                    create_server:bool=False, # make the device if it does not exist
                    load_index_from_server: bool=False,
                    persistent_storage:bool=False
                ):
        '''
        PushBullet File Server Constructor
        - `access_token` is the access token for the PushBullet account
        - `index`is an input file index to initialize with
        - `server_name` is the name of the server device on PushBullet
        - `create_server` creates a device with the name `server_name` on PushBullet if it does not already exist
        - `server_iden` is the identifier string of the server device on PushBullet
        - `load_index_from_server` is used to load the file index from the server, will only work if file index was uploaded before using `upload_file_index()` or setting `persistent_storage`
        - `persistent_storage`, set to true if push bullet server storage should be persistent (i.e. file index is saved to server and loaded from server)
        '''
        # double underscore prepend means private members and methods
        self.__access_token = access_token
        self.error_msg = '' # used to track errors
        self.__server_iden = self.__get_server_iden(server_name, server_iden, create_server)

        # if the storage is persistent, we want to upload the file index every time we do a file action
        # that way, the file index will always be the last thing uploaded to the server
        self.__persistent_storage = persistent_storage

        self.__index = {}

        if index is not None: self.__index = index
        elif load_index_from_server or persistent_storage:
            retrieved_index = self.__get_index_from_server()
            if retrieved_index is not None: self.__index = retrieved_index

    def __get_server_iden(self, name, iden, create_server):
        if iden is not None:
            return iden

        if name is not None:
            dev_info = self.get_pbfs_device(name=name)
            if dev_info is not None:
                return dev_info['iden']

            # did not find it, create server if required
            if create_server:
                return self.make_pbfs_device(name)['iden']
    
        return None

    def __make_request_header(self):
        return {'Access-Token': self.__access_token}

    def __get_index_from_server(self):
        '''
        Returns the index uploaded to the file server if any,
        Returns None if nothing was found
        '''

        # index should be last push to the server, of type note and title 'pbfs_index'
        pushes = self.get_latest_pushes(1)

        if len(pushes) == 0:
            return None

        # get the contents

        index_push = pushes[0]

        if index_push['type'] != 'note':
            # it is not a note
            return None

        if index_push['title'] != PushBulletFileServer.__INDEX_PUSH_TITLE:
            # it is not the correct title
            return None

        return eval(index_push['body'])

    def check_for_success(response:requests.Response, return_bool=False):
        # based on https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
        if not (200 <= response.status_code <= 299):
            if return_bool: return False
            # raise a bad server response error
            try:
                msg = response.json()
            except requests.exceptions.JSONDecodeError:
                msg = None
            raise exceptions.BadServerResponseError(response.status_code, message=msg)
        
        return True

    def __push(self, text=None, link: str = None, title: str=None, filepath: str =None, file=None, limit_file_size: bool = True) -> dict:
        '''
        Pushes text, URLS (links) and files to the pushbullet server
        - `filepath` is the path to the file on the local system
        - `file` is a tuple which is in the format of ( <file name>, <file binary content> )
        - `limit_file_size` is a boolean which limits file sizes to 25 MB, set to false if you use pushbullet premium
        '''
        if text is None and link is None and filepath is None and file is None:
            # Nothing to push
            raise exceptions.InvalidParameters('Nothing to push!')
        
        push_request = {
            # method is post
            'headers' : self.__make_request_header(),
            'body' : {
                'type': '',
                'url': '',
                'body': '',
                'file_name' : '',
                'file_type' : '',
                'file_url' :''
            }
        }

        push_body = push_request['body']

        if title is not None:
            push_body['title'] = 'Test Title!'

        if self.__server_iden is not None:
            push_body['source_device_iden'] = self.__server_iden

        if text is not None:
            push_body['type'] = 'note'
            push_body['body'] = str(text)

        elif link is not None:
            push_body['type'] = 'link'
            push_body['url'] = link

        elif filepath is not None or file is not None:
            if filepath is not None and file is not None:
                raise exceptions.InvalidParameters('Undetermined file source!')


            if filepath is not None:
                # check if the file exists
                if not os.path.exists(filepath):
                    raise exceptions.InvalidConfiguration(f'File "{filepath}" does not exist!')
                
                filename = os.path.split(filepath)[1]
                file_contents = open(filepath, 'rb').read()
            else:
                # we are doing file
                try:
                    filename , file_contents = file
                except ValueError:
                    raise exceptions.InvalidParameters('File tuple to push is used incorrectly!')

            file_mime_type, _ = mimetypes.MimeTypes().guess_type(filename)

            # check if its under the limit
            if limit_file_size:
                # checks if file is greater than 25 MB
                if ( (sys.getsizeof(file_contents) +33) / (1024*1024)) > 25:
                    raise exceptions.InvalidConfiguration('File size is too big!')

            # make upload request
            # by here should have filename, file_mime_type, file_contents

            response = requests.post(
                '{}/upload-request'.format(PushBulletFileServer.PUSHBULLET_API),
                headers = push_request['headers'],
                json = {
                    'file_name': filename,
                    'file_type': file_mime_type,
                }
            )

            PushBulletFileServer.check_for_success(response)

            # get upload url from upload request
            # and us to upload acutal file
            upload_response = response.json()

            upload_url = upload_response['upload_url']

            response = requests.post(
                upload_url,
                headers = push_request['headers'],
                files = {
                    'file' : file_contents
                }
            )
            PushBulletFileServer.check_for_success(response)

            # populate push body
            push_body['type'] = 'file'
            push_body['file_name'] = upload_response['file_name']
            push_body['file_type'] = upload_response['file_type']
            push_body['file_url'] = upload_response['file_url']
        
        # push the contents
        response = requests.post('{}/pushes'.format(PushBulletFileServer.PUSHBULLET_API), headers=push_request['headers'], json=push_body)
        PushBulletFileServer.check_for_success(response)

        # return good success
        return response.json()

    def __pull(self, identifier: str) -> dict:
        '''
        Returns the server contents for the given identifier.
    
        Returns dictionary which contains:
        
        `type`: the type of content for the identifier i.e. note,link or file

        `content`: The actual content, this would be the body, URL or binary file content

        `file_name`: Only included if the type is a file
        '''
        # get the response from the request
        response = requests.get('{}/pushes/{}'.format(PushBulletFileServer.PUSHBULLET_API, identifier), headers=self.__make_request_header())
        PushBulletFileServer.check_for_success(response)

        res = response.json()

        ret = {
            'type': res['type'],
            'file_name': '',
            'content': ''
        }

        if res['type'] == 'note':
            ret['content'] =  res['body']

        elif res['type'] == 'link':
            ret['content'] = ['url']

        elif res['type'] == 'file':
            # get the file content from the url
            ret['file_name'] = res['file_name']

            response = requests.get(res['file_url'])

            # return content in binary
            ret['content'] = response.content

        return ret

    def __delete(self, identifier):
        '''
        Deletes push with the given identifier
        '''
        res = requests.delete( '{}/pushes/{}'.format(PushBulletFileServer.PUSHBULLET_API, identifier), headers = self.__make_request_header())

        PushBulletFileServer.check_for_success(res)

    def __check_path( path:str):
        if not path.startswith('/'):
            raise exceptions.InvalidServerAddress(path)

    def __sanitize_path(path:str):
        '''
        Makes `path` a valid server path by:
        - Adding root address separator e.g. `path/to/file.txt` becomes `/path/to/file.txt`
        - Removing ending separator e.g. `path/to/dir/` becomes `/path/to/dir`
        - Removing multiple continuous slashes e.g. `/path//path` becomes `/path/path`
        '''

        # split the path by our address separator
        comps = path.split('/')

        # filter out the empty slots to account for multiple slashes
        sanitized_comps = list(filter(
            lambda part: part != '',
            comps
        ))

        # remake the address cleanly
        sanitized_path = '/' + '/'.join(sanitized_comps)

        return sanitized_path

    def __get_parent_dir(self, path:str, make_dirs_ok=False):
        ''' Returns the dict object in file `index` corresponding to the parent directory the given path'''
        path = PushBulletFileServer.__sanitize_path(path)
        paths = path.split('/')
        addr_stack = []
        cur_addr = self.__index

        for dir in paths[1:-1]: # not including last one as it is the leaf
            # pop the current address to the stack
            addr_stack.append(cur_addr)

            if dir == '.':
                # just pop what was last pushed to the stack
                cur_addr = addr_stack.pop()
            elif dir == '..':
                # get the upper address, pop two things from the stack
                addr_stack.pop()
                if len(addr_stack) < 1:
                       raise exceptions.UnreachableServerAddress(path)
                cur_addr = addr_stack.pop()

            else:
                cur_addr = cur_addr.get(dir)

            if cur_addr is None:
                # the directory does not exist
                if not make_dirs_ok:
                    return None

                # then we have to create the directory at the upper addrss
                if len(addr_stack) < 1:
                    raise exceptions.UnreachableServerAddress(path)

                # make directory at upper address (last item on stack)
                addr_stack[-1][dir] = {}
                cur_addr = addr_stack[-1][dir]

        return cur_addr

    # PUBLIC MEMBERS ---------------------------------------------------------------

    def get_latest_pushes(self, push_count):
        '''
        Gets `push_count` latest pushes from the server
        '''
        # index should be last push to the server, of type note and title 'pbfs_index'
        body = {
            'active': 'true',
            'limit': '{}'.format(push_count)
        }

        # make the request
        response = requests.get('{}/pushes'.format(PushBulletFileServer.PUSHBULLET_API), headers = self.__make_request_header(), params = body)

        PushBulletFileServer.check_for_success(response)

        return response.json()['pushes']

    def make_pbfs_device(self, name:str) -> dict:
        '''
        Makes a PushBullet File Server device on the Push Bullet Server
        '''
        headers =  self.__make_request_header()

        body = {
            'nickname': name,
            'model': 'PBFS v{}'.format(PushBulletFileServer.VERSION),
            'manufacturer': PushBulletFileServer.DEVICE_MANUFACTURER,
            'push_token': '',
            'icon': 'system',
            'has_sms': False
        }

        response = requests.post('{}/devices'.format(PushBulletFileServer.PUSHBULLET_API), headers=headers, json=body)
        PushBulletFileServer.check_for_success(response)

        return response.json()

    def get_pbfs_device(self, name:str=None, iden:str=None):
        '''
        Get a PushBullet File Server device from the PushBullet Server, using the device name `name` or the device identifier `iden`
        '''
        if name is None and iden is None:
            raise exceptions.InvalidParameters('No device name or device identifier')

        if name is not None and iden is not None:
            raise exceptions.InvalidParameters('Undetermined device search query (both name and identifier are set)')

        headers =  self.__make_request_header()
        
        if iden is not None:
            response = requests.get('{}/devices/{}'.format(PushBulletFileServer.PUSHBULLET_API, iden), headers=headers)
            PushBulletFileServer.check_for_success(response)

            return response.json()

        # filter by name
        response = requests.get('{}/devices'.format(PushBulletFileServer.PUSHBULLET_API), headers=headers)
        PushBulletFileServer.check_for_success(response)

        devices = response.json()['devices']

        applicable_devices = list(filter(
        lambda dev: (dev.get('manufacturer') == PushBulletFileServer.DEVICE_MANUFACTURER) and ( dev.get('nickname') == name), 
        devices))

        if len(applicable_devices) != 1:
            return None

        return applicable_devices[0]

    def delete_device(self, name:str=None, iden:str=None):
        '''
        Delete device from the PushBullet Server, using the device name `name` or the device identifier `iden`
        '''
        dev_info = self.get_device(name=name, iden=iden)
        
        if dev_info is None:
            return 0

        dev_iden = dev_info['iden']

        response = requests.delete('{}/devices/{}'.format(PushBulletFileServer.PUSHBULLET_API, dev_iden), headers=self.__make_request_header())
        PushBulletFileServer.check_for_success(response)

    def path_exists(self, path:str):
        ''' Checks if the given path exists in the index'''
        # get the parent directory if it exists
        parent_dir = None
        try:
            parent_dir = self.__get_parent_dir(path)
        except exceptions.UnreachableServerAddress:
            return None

        # the parent directory does not exist
        if parent_dir is None:
            return False

        if parent_dir.get(path.split('/')[-1]) is None:
            # file does not exist in the parent directory
            return False

        return True    

    def create_directory(self, dirpath:str):
        # creates the given directory path
        # adding throwaway so that get parent directory can handle the making of the directory
        dirpath += "/throwaway"
        parent_dir = self.__get_parent_dir(dirpath, make_dirs_ok=True)        
        return 0


    def delete_file(self, file_path: str) -> int:
        '''
        Deletes file from server at given path
        '''
        # get the file identifier and parent directory
        if not self.path_exists( file_path ):
            self.error_msg = 'File does not exist!'
            return 1
        
        filename = file_path.split('/')[-1]
        parent_dir = self.__get_parent_dir(file_path)
        file_identifier = parent_dir[filename]

        # delete the file from the server
        try:
            self.__delete(file_identifier)
        except PushBulletFileServerException as e:
            self.error_msg = 'Failed to delete file: {}'.format(e)
            return 1

        # remove the file from the index
        parent_dir.pop(filename)

        if self.__persistent_storage:
            self.upload_file_index()

        return 0

    def upload_binary_to_path(self, server_file_path: str, binary_contents) -> int:
        ''' 
        Takes absolute file path using Linux addressing, e.g /path/to/file where / is the top most directory.
        `binary_contents` is the binary contents of the file to be uploaded
        Returns the uploaded path if successful
        '''

        server_file_path = PushBulletFileServer.__sanitize_path(server_file_path)
        
        # upload the contents to the pushbullet server first, make sure that is completed
        filename = server_file_path.split('/')[-1]
        svr_response = None

        try:
            svr_response = self.__push(file=(filename, binary_contents))
        except PushBulletFileServerException as e:
            # if something went wrong, then exit with the error
            self.error_msg = 'Error: '+str(e)
            return None

        new_file_iden = svr_response['iden']

        # add the file path to the index, with the server file identifier
        parent_dir = self.__get_parent_dir(server_file_path, make_dirs_ok=True)

        # checks if there is a current file in the memory
        old_file_iden = parent_dir.get(filename)

        # if there is then delete the old file since we are overwriting it
        if old_file_iden is not None:
             # delete the file from the server
            try:
                self.__delete(old_file_iden)
            except PushBulletFileServerException as e:
                self.error_msg = 'Failed to delete file: {}'.format(e)

        # save the new file by updating the file index
        parent_dir[filename] = new_file_iden

        if self.__persistent_storage:
            self.upload_file_index()

        return server_file_path

    def download_binary_from_path(self, file_path:str):
        ''' 
        Returns binary contents of file posted to server
        '''
        # get the file identifier
        if not self.path_exists( file_path ):
            self.error_msg = 'File does not exist!'
            return None
        
        filename = file_path.split('/')[-1]
        file_identifier = self.__get_parent_dir(file_path)[filename]

        # retrieve the file contents from the pushbullet server
        ret = None
        try:
            ret = self.__pull(file_identifier)
        except PushBulletFileServerException as e:
            self.error_msg = str(e)
            return None

        return ret['content']

    def upload_file_index(self):
        '''
        Uploads the latest version of the index to the server, allows for persisitent file storage
        (Makes the server now act like actual storage instead of RAM)
        '''
        self.__push(text=str(self.__index), title=PushBulletFileServer.__INDEX_PUSH_TITLE)

    def upload_file(self,local_path, server_path):
        '''
        Uploads file at `local_path` on local device to `server_path` on server
        '''
        with open(local_path, 'rb') as file:
            return self.upload_binary_to_path(server_path, file.read())

    def download_file(self, server_path, local_path):
        '''
        Downloads file at `server_path` on server to `local_path` on local device
        '''
        with open(local_path, 'wb') as file:
            content = self.download_binary_from_path(server_path)
            if content is not None:
                file.write(content)

    def get_file_index(self):
        return dict(self.__index)

    def get_server_identifier(self):
        return self.__server_iden



# def main():
    
#     pbfs = PushBulletFileServer(ACCESS_TOKEN)
#     mime_cont = open('mime.txt', 'rb').read()

#     if pbfs.save_file('/mime.txt', mime_cont) == 0:
#         print('Save successful')
#     else:
#         print('Save Failed')
#         print('Error: {}'.format(pbfs.error_msg))

#     mime_cont = pbfs.get_file('/mime.txt')

#     if mime_cont is None:
#         print('Error: {}'.format(pbfs.error_msg))
#         return 0

#     print(mime_cont.decode('utf-8'))
    

# if __name__ == "__main__":
#     sys.exit(main())
