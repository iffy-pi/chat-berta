# Deploying Chat-Berta Web Server
This markdown is intended to cover the steps for deploying the ChatBerta web server to Heroku. It is structured with deploying a basic web server and then how to deploy made changes.

# Source(s)
The steps listed are mainly sourced from the video: https://youtu.be/4_EO4RwABbA, with some prior experience taken from the video https://youtu.be/Z1RJmh_OqeA.

**Note That Project Root Directory must be same as Git Root Directory**

# The Initial Flask App
## The Project Root Directory
This is chat-berta/

## Create A Python Virtual Environment
A virtual environment allows you to easily store all the required dependencies for your application or website, without having to mess/be interfered with by the current configurations of your system. Essentially, allowing you to make sure that your app can be deployed on any system.

First, install the virtual environment with pip:
```
pip install virtualenv
```

After installing the package, we have to create a virtual environment for the project, this is done within the project folder root directory:
```
virtualenv venv
```
Where "venv" can be replaced with the directory name we want to install virtual environment information in.


Then we can activate the environment by running its activation script, on windows it would be
```
<env directory>\Scripts\activate.bat
```
This puts us in the virtual environment terminal, installations here will not affect our own python package. 

Whenever, you are running the development server or doing any package installations, make sure to always be in the virtual environment using the activation function.

You can leave a virtual environment with the command
```
deactivate
```

## Installing Packages and Creating Requirements
First we need the flask framework which we can install (in the virtual environment):
```
python -m pip install flask
```

Next we create a requirements.txt file which lists the project dependencies, this is used by Heroku in setting up the web server for the project. This is done using the pipreqs.
```
# Install pipreqs first
python -m pip install pipreqs

# run command in root project directory
pip freeze > requirements.txt
```

pipreqs may be a good alternative in future, though it has issues with listing all the required packages. insipiration from: https://towardsdatascience.com/stop-using-pip-freeze-for-your-python-projects-9c37181730f9.

This generates chat-berta/requirements.txt. This will need to be updated each time new packages are installed for the website.

## Create Simple Flask Application
This is for the purpose of the tutorial, in this step we create a simple hello world flask application.
This is contained in the initial version of app.py:
```python
from flask import Flask

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
@app.route('/')
def index():
    return 'Hello World!'

# running the code
if __name__ == '__main__':
    # debug is true to show errors on the webpage
    app.run(debug=True)
```

## Running the app in development
You can run the developmental app, using the command:
```
flask run
```
To allow us to immediately see changes made during the root development, we can set the flask development environment variable and then run flask run
```
set FLASK_ENV=development
```
Note that this same functionality can be achieved by simply running app.py itself:
```
# replaces flask run and environment variable setting
python app.py
```

# Flask App Source Control With Git
Of course, we already have git installed and are already in a repository, so there is no problems here. Just continue as usual.

## Exclude Folders
We want to make sure we dont include the virtual environment folder and the pycache folder in the git repo, so we add those to our .gitignore in the project root directory.


# Deploying with Vercel
Vercel is a free hosting service which we can use for deploying our application.

## Create Vercel Account
Link your GitHub Account to your Vercel account by following the steps at: https://vercel.com/signup

## Link Your Git Repository
After creating your account and giving Vercel access to your git repos, select the repository you wish to deploy from the projects list (https://vercel.com/new)

## Create Vercel Build File
Next, you will need to create vercel.json, which is a JSON that tells the system how to build your project. it includes the following:
```json
{
    // 'app.py' is the root application, the starter file for the flask project
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": ".*",
      "dest": "app.py"
    }
  ]
```

## Pushing to Remote
Vercel automatically builds and re-deploys the application for every commit to our production branch: `vercel-production`

Normally, it automatically builds on deployment to the `main` branch of the GitHub project, but this can be changed by Project Settings > Git > Production Branch.

## Application URL
Application URL can be found from the Vercel Projects: https://chat-berta.vercel.app/