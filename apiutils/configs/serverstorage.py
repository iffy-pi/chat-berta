# contains configurations for the different storage configurations for the web server
import os
PBFS_ACCESS_TOKEN = os.environ.get('CHATBERTA_PBFS_ACCESS_TOKEN')
PBFS_SERVER_NAME = os.environ.get('CHATBERTA_PBFS_DEV_SVR') if os.environ.get('CHATBERTA_PBFS_DEV_SVR') is not None else 'CHATBERTA_PUSHBULLET_FILE_SERVER'
UPLOADED_CHATS_DIR = '/submitted_chats'
UPLOADED_TRANSCRIPTS_DIR = '/transcripts'
XML_CHATLOGS_DIR = '/xmlchatlogs'
JSON_CHATLOGS_DIR = '/jsonchatlogs'