from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, session
from appfuncs import *
import os

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


@app.route('/myConsole', methods=['GET', 'POST'])
def route_console():
    #tc = session['tc']
    return render_template('console.html', content='How can you see me?')


@app.route('/myConsole2', methods=['GET', 'POST'])
def route_console_2():
    #tc = TestClass('Juniper', 2)
    #session['tc'] = tc
    return redirect(url_for('route_console'))


# to download a file submitted to the server
# you can use url_for('route_download_file', filename=<filename>) to get url for specific file
@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def route_download_file(filename):
    # Appending app path to upload folder path within app root folder
    # Returning file from appended path
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

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
            
            res, filename = save_file_from_request(app.config['UPLOAD_FOLDER'], request.files['file'])
            
            if res != 0:
                return render_template('console.html', content='Something went wrong saving the file!')

            with open( get_file_path(app, filename), 'r' ) as file:
                cont = str(file.read())
            return render_template('console.html', content='File: {}'.format(cont))
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
    return render_template('chat_transcript.html')

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