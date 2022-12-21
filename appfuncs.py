# python file to contain function definitions in order to not clutter app.py

# Configure file upload parameters
# Source: https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# checks if a file is allowed to be uploaded
def allowed_file(filename):
    # allowed if not executable and is one of the allowed file extensions
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS