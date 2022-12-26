import sys
import requests
import os
import mimetypes
import json

def prettify(d: dict) -> str:
    return json.dumps(d, indent=4)

class PBFSException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class PushBulletFileServer():
    # simple file server using the pushbullet server as a save location
    PUSHBULLET_API = 'https://api.pushbullet.com/v2'
    PUSH_URL = '{}/pushes'.format(PUSHBULLET_API)
    UPLOAD_REQUEST_URL = '{}/upload-request'.format(PUSHBULLET_API)
    
    def __init__ (self, access_token, index: dict={}):
        # double underscore prepend means private members and methods
        self.__access_token = access_token
        self.__index = index
        self.error_msg = '' # used to track errors

    def http_success(http_code):
        # returns true if it was a successful request
        # based on https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
        return ( http_code >= 200 and http_code <= 299)

    def __push(self, text=None, link: str = None, filepath: str =None, file=None, limit_file_size: bool = True) -> dict:
        '''
        Pushes text, URLS (links) and files to the pushbullet server

        `filepath` is the path to the file on the local system

        `file` is a tuple which is in the format of ( <file name>, <file binary content> )

        `limit_file_size` is a boolean which limits file sizes to 25 MB, set to false if you use pushbullet premium
        '''
        if text is None and link is None and filepath is None and file is None:
            # Nothing to push
            raise PBFSException('Nothing to push!')
        
        push_request = {
            # method is post
            'headers' : {
                'Access-Token': self.__access_token
            },

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

        if text is not None:
            push_body['type'] = 'note'
            push_body['body'] = str(text)

        elif link is not None:
            push_body['type'] = 'link'
            push_body['url'] = link

        elif filepath is not None or file is not None:
            if filepath is not None and file is not None:
                raise PBFSException('Undetermined file source!')


            if filepath is not None:
                # check if the file exists
                if not os.path.exists(filepath):
                    raise PBFSException('File does not exist!')
                
                filename = os.path.split(filepath)[1]
                file_contents = open(filepath, 'rb').read()
            else:
                # we are doing file
                try:
                    filename , file_contents = file
                except ValueError:
                    raise PBFSException('File tuple used incorrectly!')

            file_mime_type, _ = mimetypes.MimeTypes().guess_type(filename)

            # check if its under the limit
            if limit_file_size:
                # checks if file is greater than 25 MB
                if ( (sys.getsizeof(file_contents) +33) / (1024*1024)) > 25:
                    raise PBFSException('File size is too big!')

            # make upload request
            # by here should have filename, file_mime_type, file_contents

            response = requests.post(
                PushBulletFileServer.UPLOAD_REQUEST_URL,
                headers = push_request['headers'],
                json = {
                    'file_name': filename,
                    'file_type': file_mime_type,
                }
            )

            if not PushBulletFileServer.http_success(response.status_code):
                raise PBFSException('Upload request failed!: {}'.format(response.json()))

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

            if not PushBulletFileServer.http_success(response.status_code):
                raise PBFSException('File upload failed!')

            # populate push body
            push_body['type'] = 'file'
            push_body['file_name'] = upload_response['file_name']
            push_body['file_type'] = upload_response['file_type']
            push_body['file_url'] = upload_response['file_url']
        
        # push the contents
        response = requests.post(PushBulletFileServer.PUSH_URL, headers=push_request['headers'], json=push_body)

        if not PushBulletFileServer.http_success(response.status_code):
            # Something failed on the server end
            raise PBFSException('Failed Push Request: {}'.format(response.json()))

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
        headers =  {
                'Access-Token': self.__access_token
        }
        response = requests.get('{}/{}'.format(PushBulletFileServer.PUSH_URL, identifier), headers=headers)

        if not PushBulletFileServer.http_success(response.status_code):
            raise PBFSException('Could not pull identifier!')

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

    def __check_path( path:str):
        if not path.startswith('/'):
            raise PBFSException('Invalid file path, must be absolute!')

    def path_exists(self, path:str):
        ''' Checks if the given path exists in the index'''
        PushBulletFileServer.__check_path(path)
        paths = path.split('/')

        cur_addr = self.__index
        upper_addr = None
        for dir in paths[1:]:
            upper_addr = cur_addr
            cur_addr = upper_addr.get(dir)

            if cur_addr is None:
                # the directory does not exist
                return False
        
        return True

    def __get_parent_dir(self, path:str, make_dirs_ok=False):
        ''' Returns the dict object in file `index` corresponding to the parent directory the given path'''
        PushBulletFileServer.__check_path(path)
        paths = path.split('/')
        cur_addr = self.__index
        upper_addr = None

        for dir in paths[1:-1]: # not including last one as it is the leaf
            upper_addr = cur_addr
            cur_addr = upper_addr.get(dir)

            if cur_addr is None:
                # the directory does not exists
                if make_dirs_ok:
                    # then we have to create the directory at the upper addrss
                    upper_addr[dir] = {}
                    cur_addr = upper_addr[dir]
                else:
                    return None

        return cur_addr
    
    def save_file(self, file_path: str, binary_contents) -> int:
        ''' 
        Takes absolute file path using Linux addressing, e.g /path/to/file where / is the top most directory.
        Returns 0 if successful
        '''
        
        # upload the contents to the pushbullet server first, make sure that is completed
        filename = file_path.split('/')[-1]
        svr_response = None

        try:
            svr_response = self.__push(file=(filename, binary_contents))
        except PBFSException as e:
            # if something went wrong, then exit with the error
            self.error_msg = str(e)
            return 1

        # add the file path to the index, with the server file identifier
        parent_dir = self.__get_parent_dir(file_path, make_dirs_ok=True)
        parent_dir[filename] = svr_response['iden']

        return 0

    def get_file(self, file_path:str):
        ''' Get file posted to the server, takes the absolute file path '''
        
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
        except PBFSException as e:
            self.error_msg = str(e)
            return None

        return ret['content']

    def get_file_index(self):
        return dict(self.__index)


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
