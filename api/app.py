import io
import mimetypes
import os
import json
import time


from flask import (Flask, flash, redirect, render_template, request, send_file,
                   session, url_for, Response)
from flask_cors import CORS 
from apiutils.functions.apifuncs import *
from apiutils.functions.PushBulletFileServer import PushBulletFileServer
from apiutils.functions.ChatParser import create_chatlog_json
from apiutils.configs.summarizer import SUMMARIZER_OPTIONS
from apiutils.configs.serverstorage import PBFS_ACCESS_TOKEN, PBFS_SERVER_NAME
from apiutils.functions.HTTPResponses import *
from apiutils.configs.summarizer import USE_ACTUAL_MODEL

if USE_ACTUAL_MODEL:
    # determines if we actually try to import the model or not
    print('Using ChatBerta model')
    from apiutils.nec.NetworkComponent import NetworkComponent as NetworkComponent

else:
    print('Using random summarizer model')
    from apiutils.nec.SimpleNetworkComponent import SimpleNetworkComponent as NetworkComponent

# initialize app flask object
# intializing to the name of the file
app = Flask(__name__)
# https://stackoverflow.com/questions/20035101/why-does-my-javascript-code-receive-a-no-access-control-allow-origin-header-i
CORS(app)

# Load app configuration from config.py, must be at root of repository
# Source: https://exploreflask.com/en/latest/configuration.html
app.config.from_pyfile(os.path.join('..', 'apiutils', 'configs', 'apiconfig.py'))

# App routing information
    # now we use app routing to map a function to a given page of our website
    # in app routing, it starts from the root of our website
    # so if our website is mysite.com, and we wanted to route to mysite.com/hello
    # we would pass /hello to the app route call
    # app routing uses special @ and then the flask app oobject
    # then we immediately define the associated function for the URL
    # @app.route("/test")
    # def testfunc():
    #     return "Testing web page!"
    # we can have several routes for the different pages on our website
    # just by adding more app routes and the subsequent functions that handle them

if PBFS_ACCESS_TOKEN is None:
    raise Exception('PushBullet File Server Access Token')

pbfs = PushBulletFileServer(PBFS_ACCESS_TOKEN, server_name=PBFS_SERVER_NAME, create_server=True)
nec = NetworkComponent()

# UTILITIES --------------------------------------------------------------------------------------------------------
@app.route('/myConsole', methods=['GET', 'POST'])
def route_console():
    return render_template('console.html', content=app.config['ALLOWED_EXTENSIONS'])


# to download a file submitted to the server
# you can use url_for('route_download_file', filename=<filename>) to get url for specific file
@app.route('/uploads/<path:filepath>', methods=['GET', 'POST'])
def route_download_file(filepath):
    # Appending app path to upload folder path within app root folder
    # Returning file from the pushbullet file server
    pbfs_file_path = '/{}'.format(filepath)
    file_content = pbfs.download_binary_from_path(pbfs_file_path)

    if file_content is None:
        return '{}\n{}'.format(pbfs_file_path, pbfs.get_file_index())

    return send_file(
        io.BytesIO(file_content),
        download_name=filepath.split('/')[-1],
        mimetype = mimetypes.MimeTypes().guess_type(filepath.split('/')[-1])[0],
        as_attachment=True
    )

# DEPRECATED FLASK BASED FRONT END CALLS ----------------------------------------------------------------------------------------------------
# receives parameters from the chat submitted page and calls the summarizer on it
@app.route('/summarize/<source>/<tag>/<options>')
def route_summarize(source, tag, options):
    # get the text
    text = get_chatlog_json(pbfs, tag)
    
    if text is None:
        return render_template('console.html', content='No valid source found!, {}'.format(pbfs.get_file_index()))
    
    return render_template('summarizer_results.html', source=source, text=text, options=options)


# page that we go to when summarize button is clicked
@app.route('/chatSubmitted', methods=['POST', 'GET'])
def route_chat_submitted():
    # handles the multiple submission sources as well as the submission options
    summarizer_options = []
    if request.method == 'POST':
        # parse the summarizer options
        # get all the summarizer opt keys
        summarizer_options = list( filter( 
            lambda key: key.startswith('summarizer_opt_'),
            request.form
        ))
        # remove the summarizer opt tag
        summarizer_options = [ o.replace('summarizer_opt_', '') for o in summarizer_options ]

        source = None
        tag = None
        chatlog_json = None
        # check for the transcript file
        transcript_text = request.form.get('transcript_text')
        if transcript_text:
            # handle the transcript text
            # save the file
            source = 'text'
            try:
                chatlog_json = create_chatlog_json(transcript_text)
            
            except Exception as e:
                return render_template('console.html', content="Transcript Parsing Error: {}".format(e))

        # check for the file in the request
        elif 'chatfile' in request.files:
            # save the chat file
            source = 'file'
            chatfile = request.files['chatfile']

            # check the chatfile
            if not safe_request_file(chatfile):
                return render_template('console.html', content='Invalid chatfile')

            # get the content
            chatfile_str = chatfile.read().decode('utf-8')

            try:
                chatlog_json = create_chatlog_json(chatfile_str)
            except Exception as e:
                return render_template('console.html', content="Parsing Error: {}".format(e))

        if source is not None:
            # create Network Component object to process summarization
            nec = NetworkComponent()
            nec.generate_summary(chatlog_json)
            # save the json file to specified folder
            res, tag = save_chatlog_json(pbfs, nec.json)
            if res != 0:
                 return render_template('console.html', content='Something went wrong saving the file!')

            # we found something saved, so redirect to the summarizer page
            return redirect( url_for('route_summarize', source=source, tag=tag, options=make_summarizer_opt_str(summarizer_options)))

        # nothing was found
        return render_template('console.html', content='No content was submitted!')
    else:
        return render_template('console.html', content='Invalid, should not get here!')

# flask submit a chat page
@app.route('/submitChat', methods=['POST', 'GET'])
def route_submit_chat():
    options = SUMMARIZER_OPTIONS
    return render_template('submit_chat.html', opts=options)


# REACT API CALLS ----------------------------------------------------------------------------------------------------
# called by react frontend with populated JSON fields
@app.route('/api/submit-chat', methods=['POST', 'GET'])
def route_api_submit_chat():
    if request.method != 'POST':
        return error_response(400, message='Invalid HTTP method!')

    # Expecting the following keys
    # summary options and chat package
    # request.json should be in format of apiutils/samples/sample_api_request_1.json
    if request.json is None:
        return error_response(400, message='No JSON content included!')

    expected_keys = [ 'summary_options', 'chat_package']

    missing_keys = list(filter(
        lambda key: key not in request.json,
        expected_keys
    ))

    if len(missing_keys) > 0:
        return error_response(400, message="Required keys are missing: {}".format(missing_keys))

    # then retrieve the items
    summary_options = request.json['summary_options']
    chat_package = request.json['chat_package']

    # call the network component to generate the summary chat package
    res, summary_chat_package = nec.summarize( chat_package, summary_options )

    if res != 0:
        return error_response(500, message="Summarization process failed on server")

    # send the response back to the server
    js = {
        'summary_options': summary_options,
        'chat_package': summary_chat_package
    }

    resp = make_json_response(js)
    return resp

@app.route('/api/sample', methods=['POST', 'GET'])
def route_sample_resp():
    faddr = os.path.join ( os.path.split(__file__)[0], '..',  'apiutils', 'samples', 'sample_raw_chat_1.txt')
    with open(faddr) as file:
            chat_package = json.loads(create_chatlog_json( str(file.read())))


    summary_options = {
        "basic_options": [ "strictSummarize", "treatAsMonologue"],
        "summarize_only_for": -1 
    }

    # use random summarizer
    res, summary_chat_package = nec.summarize( chat_package, summary_options )

    if res != 0:
        return error_response(500, message="Summarization process failed on server")

    # for now craft a simple relay message
    js = {
        'summary_options': summary_options,
        'chat_package': summary_chat_package
    }

    time.sleep(1) # to simulate server latency when in development

    resp = make_json_response(js)
    return resp

# ----------------------------------------------------------------------------------------------------
# for the root of the website, we would just pass in "/" for the url
@app.route('/')
def index():
    # render index html which contains the form
    # form submission will route to /submitForm
    return render_template('index.html')

# running the code
if __name__ == '__main__':
    # debug is true to show errors on the webpage
    app.run(debug=True)