# Application configuration file
# Imported to app config in app.py
# Source: https://exploreflask.com/en/latest/configuration.html
import os
from apiutils.configs.sharedconfig import SHARED_CONFIG
def get_secret_key():
    # secret key was generated with command: python -c "import secrets; print(secrets.token_hex())"
    # Then store it in your environment variables with the below name
    return os.environ.get('CHATBERTA_SECRET_KEY')


# Source: https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
UPLOAD_FOLDER = 'uploads' # configure upload folder
ALLOWED_EXTENSIONS = SHARED_CONFIG['ALLOWED_EXTENSIONS']
SECRET_KEY = get_secret_key()