# python file to contain function definitions in order to not clutter app.py
import hashlib
import os
import time

from api.config import ALLOWED_EXTENSIONS
from utils.PushBulletFileServer import *
from werkzeug.utils import secure_filename


class TestClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def string(self):
        return '(a = {}, b={})'.format( self.a, self.b)

SUMMARIZER_OPTIONS = [
    ('UseStrict', 'Strict summary'),
    ('TreatAsMonologue', 'Treat transcript as monologue')
]

UPLOADED_CHATS_DIR = '/submitted_chats'
UPLOADED_TRANSCRIPTS_DIR = '/transcripts'
XML_CHATLOGS_DIR = '/xmlchatlogs'

def make_summarizer_opt_str(opt:list) -> str:
    if len(opt) < 1: return 'NoOpts'
    optstr = opt.pop(0)
    for o in opt:
        optstr += ',{}'.format(o)

    return optstr

def parse_summarizer_opt_str(optstr:str) -> list:
    if optstr == 'NoOpts':
        return []

    return optstr.split(',')

def gen_unique_tag():
    ''' Generates a unique hashed tag based on the current unix time '''
    return hashlib.md5( str(time.time()).encode() ).hexdigest()

# checks if a file is allowed to be uploaded
def allowed_file(filename):
    # allowed if not executable and is one of the allowed file extensions
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def safe_request_file(request_file):
    # checks a request file, returns 0 if it is safe
    if request_file.filename == '':
        return False

    if not request_file or not allowed_file(request_file.filename):
        return False
        
    return True

def save_file_from_request(pbfs:PushBulletFileServer, request_file, pbfs_file_path: str =None):
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    file = request_file
    
    if not safe_request_file(file):
        return ( -1, None)

    # save the file into the pushbullet file server
    pbfs_file_path  = pbfs.upload_binary_to_path(pbfs_file_path, file.read())
    res = 1 if pbfs_file_path is None else 0
    return ( res, pbfs_file_path )


def save_uploaded_chat_file(pbfs:PushBulletFileServer, request_file ):
    # saves the uploaded chat file and returns the file name for the
    file_tag = gen_unique_tag()
    pbfs_file_path = '{}/{}.txt'.format(UPLOADED_CHATS_DIR,file_tag)

    # save the file
    res, _ = save_file_from_request(pbfs, request_file, pbfs_file_path=pbfs_file_path)

    return ( res, file_tag )

def save_transcript_text(pbfs:PushBulletFileServer, transcript_text:str ):
    file_tag = gen_unique_tag()
    pbfs_file_path = '{}/{}.txt'.format(UPLOADED_TRANSCRIPTS_DIR,file_tag)

    # save the text to file
    fpath = pbfs.upload_binary_to_path(pbfs_file_path, transcript_text.encode())
    res = 1 if fpath is None else 0

    return ( res, file_tag )

def get_text_for_file(pbfs:PushBulletFileServer, pbfs_file_path:str ):
    ''' Returns text in an uploaded text file '''
    contents = pbfs.download_binary_from_path(pbfs_file_path)

    if contents is None:
        return None

    return contents.decode('utf-8')

def get_source_text(pbfs:PushBulletFileServer, source:str, tag:str) -> str:
    # gets the text in the file uploaded to the tag
    possible_source_dirs = {
        'text': UPLOADED_TRANSCRIPTS_DIR,
        'file': UPLOADED_CHATS_DIR
    }

    if source not in possible_source_dirs.keys():
        raise Exception('Unknown source: {}'.format(source))

    return get_text_for_file(pbfs, '{}/{}.txt'.format(possible_source_dirs[source], tag))

def save_chatlog_xml(pbfs:PushBulletFileServer, chatlog_xml:str ):
    file_tag = gen_unique_tag()
    pbfs_file_path = '{}/{}.xml'.format(XML_CHATLOGS_DIR ,file_tag)

    # save the text to file
    fpath = pbfs.upload_binary_to_path(pbfs_file_path, chatlog_xml.encode())
    res = 1 if fpath is None else 0

    return ( res, file_tag )

def get_chatlog_xml(pbfs:PushBulletFileServer, tag:str) -> str:
    return get_text_for_file(pbfs, '{}/{}.xml'.format(XML_CHATLOGS_DIR, tag))