import io
import mimetypes
import os

from flask import (Flask, flash, redirect, render_template, request, send_file,
                   session, url_for)
from api.frontend.appfuncs import *
#from api.frontend.PushBulletFileServer import *
#from middleware.chat_handling import create_chatlog_xml

# initialize app flask object
# intializing to the name of the file
app = Flask(__name__, instance_relative_config=True)

# Load app configuration from config.py, must be at root of repository
# Source: https://exploreflask.com/en/latest/configuration.html
app.config.from_object('config')

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

acc_token = os.environ.get('CHATBERTA_PBFS_ACCESS_TOKEN')
dev_svr = os.environ.get('CHATBERTA_PBFS_DEV_SVR')

pbfs = PushBulletFileServer(acc_token, server_name=(dev_svr if dev_svr is not None else 'CHATBERTA_PUSHBULLET_FILE_SERVER'), create_server=True)


@app.route('/myConsole', methods=['GET', 'POST'])
def route_console():
    return render_template('console.html', content=gen_unique_tag())


@app.route('/testPage', methods=['GET', 'POST'])
def route_console_2():
    if request.method == 'POST':
        # st = ''
        # for key in request.form:
        #     st = '{},{}'.format(st, request.form[key])
        return render_template('console.html', content=str(request.form))

# page when the chat dialog (transcript or file) is submitted
@app.route('/dialogSubmitted', methods=['POST', 'GET'])
def route_dialog_submitted():
    if request.method == 'POST':
        if request.args['source'] == 'transcript':
            # handle chat transcript form
            # using the name attribute of the text input tag in index.html
            transcript_text = request.form['dialog_text_box']
            return render_template('console.html', content='The text: {}'.format(transcript_text))

        elif request.args['source'] == 'file':
            # check if the request has the file part
            if 'file' not in request.files:
                return render_template('console.html', content='No file provided!')
            
            res, filename = save_file_from_request(pbfs, request.files['file'], pbfs_file_path='/sample-chat.txt')
            
            if res != 0:
                return render_template('console.html', content='Something went wrong saving the file!')

            # with open( get_file_path(app, filename), 'r' ) as file:
            #     cont = str(file.read())
            return render_template('console.html', content=filename)
        else:
            return render_template('console.html', content='{}-{}'.format(request.args, request.mimetype))
    else:
        return render_template('console.html', content='Invalid, should not get here!')

# submit chat transcript text
@app.route('/ChatFile', methods=['POST', 'GET'])
def route_chat_file():
    return render_template('chat_file.html')

# submit chat transcript text
@app.route('/ChatTranscript', methods=['POST', 'GET'])
def route_chat_transcript():
    options = SUMMARIZER_OPTIONS
    return render_template('chat_transcript.html', opts=options)

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

# receives parameters from the chat submitted page and calls the summarizer on it
@app.route('/summarize/<source>/<tag>/<options>')
def route_summarize(source, tag, options):
    # get the text
    text = get_chatlog_xml(pbfs, tag)
    
    if text is None:
        return render_template('console.html', content='No valid source found!, {}'.format(pbfs.get_file_index()))
    
    return render_template('summarizer_results.html', source=source, text=text, options=options)

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
        chatlog_xml = None
        # check for the transcript file
        transcript_text = request.form.get('transcript_text')
        if transcript_text:
            # handle the transcript text
            # save the file
            source = 'text'
            try:
                chatlog_xml = create_chatlog_xml(transcript_text)
            
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
                chatlog_xml = create_chatlog_xml(chatfile_str)
            except Exception as e:
                return render_template('console.html', content="Parsing Error: {}".format(e))

        if source is not None:
            # save the xml file in the right location
            res, tag = save_chatlog_xml(pbfs, chatlog_xml)
            if res != 0:
                 return render_template('console.html', content='Something went wrong saving the file!')

            # we found something saved, so redirect to the summarizer page
            return redirect( url_for('route_summarize', source=source, tag=tag, options=make_summarizer_opt_str(summarizer_options)))

        # nothing was found
        return render_template('console.html', content='No content was submitted!')
    else:
        return render_template('console.html', content='Invalid, should not get here!')

# submit a chat
@app.route('/submitChat', methods=['POST', 'GET'])
def route_submit_chat():
    options = SUMMARIZER_OPTIONS
    return render_template('submit_chat.html', opts=options)

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