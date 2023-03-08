# Chat-Berta
Chat-Berta Project File.

This also serves as the repository for ELEC498 Group 12 (JISH).

Chat-Berta is an application with a React frontend and Flask backend.

# Repository Organization
This repository contains files used for both the frontend and the backend.

The files and directories used for the React frontend are:
```
root
|  public/
|  src/
|  package-lock.json
|  package.json
```
These were created using `create-react-app` and then edited as appropriate. The main folder of interest will be src/ as it contains all the source code for the React components and other JS configurations.

The files and directories used for the Flask backend are:
```
root
|  api/
|  apiutils/
|  src/shared/
|  requirements.txt
|  vercel.json
```

Note that src/shared/ contains JSON data files that are used by both React and Flask, it is located within src to support React imports!

The remaining files would be:
```
root
|  server-void/
|  docs/
|  git-pr.bat
|  promote.bat
```
server-void/ contains files that are not relevant for the entire application. This includes simple READMEs and notes, as well as prototype models and such. **All files required by the server can NEVER be put in server-void/**

# The Deployment Configuration
The entire web server is split into the React frontend (APP) and the Flask Backend (API). These are deployed **separately** into different vercel productions.

- http://chat-berta.vercel.app/ is the deployment for the APP (React Frontend)
- http://chat-berta-api.vercel.app/ is the deployment for API (Flask backend)

Following this, each deployment has their own assigned branch in the repository:
- `app-vercel-production` is the production branch for the APP deployment
- `api-vercel-production` is the production branch for the API deployment

The development workflow is to merge commits into `main` and then merge from `main` to any of the production branches.

**⚠️NEVER MERGE THE PRODUCTION BRANCHES INTO MAIN, THEY HAVE COMMITS SPECIFICALLY CONFIGURED FOR PRODUCTION⚠️**

**⚠️NEVER MERGE DIRECTLY TO THE PRODUCTION BRANCHES, YOU SHOULD ONLY MERGE FROM MAIN INTO THE PRODUCTION BRANCHES⚠️**

**⚠️NEVER COMMIT DIRECTLY TO THE PRODUCTION BRANCHES, YOU SHOULD ONLY MERGE FROM MAIN INTO THE PRODUCTION BRANCHES⚠️**

## Vercel Project Management
The vercel projects are under Iffy's Vercel account:
- https://vercel.com/iffy-pi/chat-berta-api
- https://vercel.com/iffy-pi/chat-berta

Sign in is with Git.

## Deployment To Production Website (Promotion)
As said before, we only deploy from `main`. We do deployments by merging main to `app-vercel-production` and `api-vercel-production`. This will mean 2 pull requests: one for the app, and one for the api.

You can use the below links to quickly initiate a pull request:

| Deployment Type |Pull Request URL |
|------------------------|----------------------------------------------------------------------------|
| APP (React) deployment | https://github.com/iffy-pi/chat-Berta/compare/app-vercel-production...main |
| API (Flask) deployment | https://github.com/iffy-pi/chat-Berta/compare/api-vercel-production...main |

Alternatively, you can also use promote.bat to quickly launch either of these pages from the command line.

Deploy React frontend:
```
promote app
```
Deploy Flask backend:
```
promote api
```

## About vercel.json
vercel.json is used in the API deployment to override the default React build process vercel uses and instead build the Flask backend.

This file is not present on the app-vercel-production branch since we want Vercel to build the actual react application. As a result, it was deleted directly from the branch by commit [afa86ea21db05f4f819323b642f6dfc0ea3a5c56](https://github.com/iffy-pi/chat-berta/commit/afa86ea21db05f4f819323b642f6dfc0ea3a5c56).

**Note that commit afa86ea21db05f4f819323b642f6dfc0ea3a5c56 only exists on `app-vercel-production` as it is the specific requirement for that production branch.**

## Previous Deployments
January 25 2022: Iffy deployed bare bones React frontend

# Development Workbench Requirements
You will need the following to work on the repository and use the development server.

## Programs and Applications
1. Python (https://www.python.org/downloads/)
2. Node.js (https://nodejs.org/en/download/)

## Environment Variables
1. The environment variable `CHATBERTA_PBFS_ACCESS_TOKEN`, used for accessing the pushbullet file server (contact Iffy for environment variable value)
2. The environment variable `CHATBERTA_SECRET_KEY`, used for setting the server session key, (contact Iffy for environment variable value)
3. The environment variable set `CHATBERTA_PBFS_DEV_SVR` to `ChatBerta-PBFS-Dev-Server`

# Running The Development Application
## Running the backend (Flask)
1. Start your virtual environment
```
venv\Scripts\activate
```

2. Set the development state to debug by setting the `FLASK_DEBUG` environment variable. This will allow flask to automatically reload when changes are made to the source code.
```
set FLASK_DEBUG=1
```

3. Go into the api/ directory and run `flask run`
```
cd api
flask run
```
Note: You may need to install python packages required before you can run flask, if you get a missing package error run the following command:
```
pip install -r requirements.txt
```

Note: The frontend is expecting the API to be at http://localhost:5000. This is the default port flask starts on anyway, however if you need to manually set it, set the environment variable `FLASK_RUN_PORT` to `5000` before running the application.

## Running the frontend (React)
1. Open the root directory of the repo and run `npm start`. (`npm` is from Node.js).
```
npm start
```

# Development Workflow
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

You can test your changes in the development application (See the steps above)

**Have a file that is used by both React and Flask? Place it in src/shared and access it from there!**

## Push Branch
Push all your commits by using the command:
```
git push
```
Note: You can make more commits and push as usual until you are ready to merge with the main branch.

## Merge With Main (if you created a development branch)
Merge your branch with the mainline by initiating a pull request, this can be done using the added utility git-pr.bat:
```
git-pr.bat
```
Enter `Y` to open a pull request and make sure to select `main` as the branch to merge with.
Ideally, we should review merges to the mainline, but this may not be guaranteed.