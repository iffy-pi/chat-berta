# python file to contain function definitions in order to not clutter app.py
from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS
import time
import os

class TestClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def string(self):
        return '(a = {}, b={})'.format( self.a, self.b)

def get_secret_key():
    return 'ababa'

# checks if a file is allowed to be uploaded
def allowed_file(filename):
    # allowed if not executable and is one of the allowed file extensions
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_path(app, filename):
    # creates the filename for the file on the server, gotten from the upload folder
    return os.path.join( app.config['UPLOAD_FOLDER'], filename)


def save_dialog_transcript(app, transcript_text):
    # save dialog transcript text to a temp file in the upload folder and return the filename
    transcript_fname = os.path.join ( 'temp', 'transcript_{}.txt'.format( str(time.time()).replace('.','') ))
    full_path = os.path.join( app.config['UPDATE_FOLDER'], transcript_fname)

    # make the relevant directories
    os.makedirs(os.path.split(full_path)[0], exist_ok=True)
    # save the file

def save_file_from_request(upload_folder, request_file):
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    file = request_file
    if file.filename == '':
        return ( -1, None )

    if not file or not allowed_file(file.filename):
        # file is not present or file is not allowed
        return (-2, None)

    # save the file and render the file contents
    filename = secure_filename(file.filename)
    file.save( os.path.join( upload_folder, filename))
    
    return ( 0, filename )