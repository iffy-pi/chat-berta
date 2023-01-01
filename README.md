# Chat-Berta
Chat-Berta Project File.

This also serves as the repository for ELEC498 Group 12 (JISH)

## Directory Information:
This entire repository is used to package the web application for Chat-Berta. This means most of the files here are all useful for the web server.

deploy-web-server.md contains information on how to deploy the web server (during its initial creation) and is archived as a good source of informaiton.

git-pr.bat is a simple batch script that streamlinees the opening of pull requests for the application.

server-void/ contains files and folders that are not relevant to the web server. That is the web server can be deployed without the files in this folder. **All files required by the server can NEVER be put in server-void/**

# Development Workbench Requirements
You will need the following to work on the repository and use the development server.

## Environment Variables
1. The environment variable `CHATBERTA_PBFS_ACCESS_TOKEN`, used for accessing the pushbullet file server (contact Iffy for environment variable value)
2. The environment variable `CHATBERTA_SECRET_KEY`, used for setting the server session key, (contact Iffy for environment variable value)
3. The environment variable set `CHATBERTA_PBFS_DEV_SVR` to `ChatBerta-PBFS-Dev-Server`

# Running The Web Serevr
To run the developmental web server, first you must start up your virtual environment:
```
venv\Scripts\activate
```
Note: You should always be working in the virtual environment for the most part.

Next, run the command `flask run` in the api/ directory:
```
cd api
flask run
```

Note: You can set the environment variable `FLASK_DEBUG=1` to have the web server automatically reload when changes are made to the file:
```
set FLASK_DEBUG=1
```

# Standard Commits (No Web App Deployments)
**Make sure you have fulfilled all the requirements for a development workbench**

This is the case where there are no deployments to the Vercel web app, i.e. standard changes to the repository. This can be handled by making pushes to the main branch of the repo (i.e. `main`), however as there are multiple people working on things, extensive changes should be handled in separate branches and then merged with the main branch.


## Pull Latest Changes from mainline
Switch to mainline branch if you are not on there already:
```
git checkout main
```
Then pull
```
git pull
```

## Create Developmental Branch (if applicable)
Use a development branch if you are doing extensive changes. Create a new development branch of the current branch (main) with a name in the format: `<dev>/<username>/<description>` e.g.
```
git checkout -b dev/iffy-pi/sample-dev-branch
```

Branches allow you to continue experimental work without interfering with the working code in mainline.

## Make your changes and commits
Note that whenever you install new packages, be sure to reupdate the requirements file with:
```
pip freeze > requirements.txt
```

You can test changes by using the developmental server (within virtual environment):
```
python app.py
```

Commit changes to your branch if you created one, or the main branch as follows.

## Push Branch
Push all your commits by using the command:
```
git push
```
Note: You can make more commits and push as usual until you are ready to merge with the main branch.

## Merge With Main (if you created a developmental branch)
Merge your branch with the mainline by initiating a pull request, this can be done using the added utility git-pr.bat:
```
git-pr.bat
```
Enter `Y` to open a pull request and make sure to select `main` as the branch to merge with.
Ideally, we should review merges to the mainline, but this may not be guaranteed.

## Web App Deployments
In this case, we deploy contents from the `main` branch to the Vercel app, this can be done by merging the contents of the `main` branch, to `vercel-production`.

1. Go to https://github.com/iffy-pi/Chat-Berta/compare/vercel-production...main to initiate a pull request that merges `main` commits into `vercel-production`
2. Give PR a useful title
3. Merge the pull request
