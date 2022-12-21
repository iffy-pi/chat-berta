from flask import Flask, render_template, request, redirect

# initialize app flask object
# intializing to the name of the file
app = Flask(__name__)

# now we use app routing to map a function to a given page of our website
# in app routing, it starts from the root of our website
# so if our website is mysite.com, and we wanted to route to mysite.com/hello
# we would pass /hello to the app route call

# app routing uses special @ and then the flask app oobject
# then we immediately define the associated function for the URL
@app.route("/test")
def testfunc():
    return "Testing web page!"

# we can have several routes for the different pages on our website
# just by adding more app routes and the subsequent functions that handle them

# for the root of the website, we would just pass in "/" for the url
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # handle chat transcript form
        return render_template('console.html', content='Test')
    else:

        return render_template('index.html', message='Hello World! I am Chat-Berta! Be afraid.')

# running the code
if __name__ == '__main__':
    # debug is true to show errors on the webpage
    app.run(debug=True)