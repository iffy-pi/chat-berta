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

# Deploying With Heroku
Heroku is chosen because it handles all the nitty gritty stuff like infrastructure, DNS and all that for small simple projects such as this one.

## Create a Heroku Account
Create a free heroku account using https://signup.heroku.com/

## Install the Heroku CLI
Install the Heroku CLI using the steps contained in: https://devcenter.heroku.com/articles/heroku-cli

## Log into your Heroku Account
You will need to log into your heroku account using the CLI, with the command below:
```
heroku login
```

## Create Procfile
First we create a procfile, that tells heroku how to run the app.

Create a file names `Procfile` (case sensitive) and place the following line:
```
web: gunicorn app:app
```

The general format for this line is
```
web: gunicorn <module-name>:<app-name>
```

Where `<module-name>` is the name of the module or file that holds your main flask controller file, and `<app-name>` is the name of your flask app.

In this case, the module name is app because the flask code is in the file app.py, and the app name is app, because that’s what we called it in the file (when we created our flask app object)

The Procfile tells Heroku to serve our web app using Gunicor, a WSGI HTTP server which is compatible with various web frameworks including Flask.

Next we install gunicorn and update our requirements file:
```
pip install gunicorn==20.0.4
pip freeze > requirements.txt
```

Make sure to update the requirements.txt file on the repository.

## Create Heroku Application
We want to create the production version of our app on the Heroku end, so we do this using heroku create, in this case we specify the app name as last argument:
```
heroku create chat-berta
```

## Pushing To Remote
Now we have created our app, we can push our changes to the Heroku remote by specifying the Heroku remote in our push command.

Link to the app you created using the below command (This will not be required if you did `heroku create` in the same repository),
```
heroku git:remote -a chat-berta
```

```
git push heroku main
```

Where `main` is the branch we are pushing from.

## Application URL
Whenever you push to Heroku remote, your application URL is at the bottom of the build log.

You can also open your app website using the command `heroku open`.


# Development Pipeline
This is intended to cover the general steps for making changes to the app.

First start up the virtual environment using:
```
venv\Scripts\activate.bat
```

## Simple Changes
This is for simple changes that we are **100% sure do not need extensive verification**. This would be something as simple as a character change. For more extensive changes, refer to the Big Changes section.

### Pull Latest Changes from mainline
Switch to mainline branch if you are not on there already:
```
git checkout main
```

Then pull:
```
git pull
```
### Change The Application Source Code
This can be any amount of changes we want, in this case we just do a simple change to the network message.

Note that whenever you install new packages, be sure to reupdate the requirements file with:
```
pip freeze > requirements.txt
```

### Test on the development server
Run the application with `python app.py` to test your changes on a developmental server.

### Commit Changes
Commit whatever changes you made to the branch you are working on.
```
git commit app.py -m "Simple test change!"
```
Make as many commits as you need.

### Push Commits To Main Branch
Push all your commits by using the command:
```
git push
```

### Deploy to Heroku
Push to the Heroku remote.
```
git push heroku main
```



## Big Changes
### Pull Latest Changes from mainline
Switch to mainline branch if you are not on there already:
```
git checkout main
```

Then pull
```
git pull
```

### Create Developmental Branch
Create a new development branch of the current branch (main) with a descriptive name
```
git checkout -b iffy-sample-dev-branch
```

**Make sure to always include your name as the first part of the branch name**

Branches allow you to continue experimental work without interfering with the working code in mainline.

### Change The Application Source Code
This can be any amount of changes we want, in this case we just do a simple change to the network message.

Note that whenever you install new packages, be sure to reupdate the requirements file with:
```
pip freeze > requirements.txt
```

### Test on the development server
Run the application with `python app.py` to test your changes on a developmental server.

### Commit Changes
Commit whatever changes you made to the branch you are working on.
```
git commit app.py -m "Simple test change!"
```
Make as many commits as you need.

### Push Branch
Push all your commits by using the command:
```
git push
```
Note: You can make more commits and push as usual until you are ready to merge with the main branch.

### Merge With Main
Merge your branch with the mainline by initiating a pull request, this can be done using the added utility git-pr.bat:
```
git-pr.bat
```
Enter `Y` to open a pull request and make sure to select `main` as the branch to merge with.
Ideally, we should review merges to the mainline, but this may not be guaranteed.

### Deploy to Heroku
Go back to the main branch and pull changes from the remote and then push to the Heroku remote.
```
git checkout main
git push heroku main
```