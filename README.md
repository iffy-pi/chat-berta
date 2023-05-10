# Chat-Berta
The purpose of this project is to design a tool (Chat-Berta) which can perform extractive summarization on chat box dialog using machine learning models. Chat bots have become increasingly common in online platforms and customer services, so there arises a need to efficiently obtain the key points of any given dialogue to optimize analyses. The tool is intended to provide more privacy, visualization, and a client-centric focus to summarization than that provided by tools such as ChatGPT.

The goal of the tool is to perform extractive summarization of text files or raw text, where the summarization results indicate which messages contributed to the summary. The tool was designed as a Frontend Component (FEC) and Network Component (NC) which handles user input and summarization processing respectively, independently from one another.

The tool implementation closely follows this design approach and is implemented as a web application. The frontend of the web app represents the FEC and was implemented with React.js and CSS. It handles user input and converts them into an API request sent to the backend, which represents the NC. The API is built with Flask and services requests by invoking the implemented network component object that contains the summarization model. The network component uses the model to perform the summary, and packages the model output for the FEC. The FEC renders the response as a full summary paragraph and a chat pane of the input transcript which highlights messages used in the summary.

The ML model is implemented with PyTorch and is an extension RoBERTa, the robustly optimized BERT language model. The model identifies the k most important sentences in the dialogue, which are combined to form the summary. Sentence importance is determined using ROUGE scores, a training metric that compares the model's selected sentences against sentences selected for a reference summary. This was used with MSE loss and the SAMSum dataset to train the model.

The tool was able to meet speed requirements, with an end-to-end response time of 10 seconds. The FEC and NC were tested and verified to appropriately handle erroneous user input and requests, as well as block malicious attacks. As for the model, its performance was evaluated using ROUGE metrics, where it achieved a recall of 0.32, precision of 0.17 and f1 measure of 0.22. This is significantly below SOTA performance, which averages 0.4 to 0.5 in f1.

While the tool satisfies the defined goals, there is room for improvement. The web app GUI can be optimized for mobile devices, and API performance can be improved by resolving resource contention in request servicing. The training pipeline and loss function of the summarization model can also be refined to improve its summarization quality, while more capable hardware can improve its processing speed.

See the full report [here](docs/Final_Report.pdf)


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
- `production/app` is the production branch for the APP deployment
- `production/api` is the production branch for the API deployment

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
As said before, we only deploy from `main`. We do deployments by merging main to `production/app` and `production/api`. This will mean 2 pull requests: one for the app, and one for the api.

You can use the below links to quickly initiate a pull request:

| Deployment Type |Pull Request URL |
|------------------------|----------------------------------------------------------------------------|
| APP (React) deployment | https://github.com/iffy-pi/chat-berta/compare/production/app...main?expand=1 |
| API (Flask) deployment | https://github.com/iffy-pi/chat-berta/compare/production/api...main?expand=1 |

Alternatively, you can also use promote.bat to quickly launch either of these pages from the command line.

Deploy React frontend:
```
promote app
```
Deploy Flask backend:
```
promote api
```
## Specific Frontend/Backend Deployment Settings
### vercel.json
vercel.json is used in the API deployment to override the default React build process vercel uses and instead build the Flask backend.

This file is not present on the production/app branch since we want Vercel to build the actual react application. As a result, it was deleted directly from the branch by commit [8a0c81b4c9b0c9722f4447f237ab5e486678c687](https://github.com/iffy-pi/chat-berta/commit/8a0c81b4c9b0c9722f4447f237ab5e486678c687).

**Note that commit 8a0c81b4c9b0c9722f4447f237ab5e486678c687 only exists on `production/app` as it is the specific requirement for that production branch.**

### APP vercelignore
The frontend is React and therefore does not need the Python packages specified in requirements.txt. This is achieved by adding requirements.txt to the .vercelignore as a specific commmit in the frontend promotion branch (production/app).

The specific commit is: [af7290d](https://github.com/iffy-pi/chat-berta/commit/af7290d)

**Note that commit af7290d only exists on `production/app` as it is the specific requirement for that production branch.**

### API vercelignore
The backend is just the Flask API and does not need to use the React files. Therefore React files and folders were added to vercelignore on commit [8397f3b](https://github.com/iffy-pi/chat-berta/commit/8397f3b).

**Note that commit 8397f3b only exists on `production/api` as it is the specific requirement for that production branch.**

# Development Workbench Requirements
You will need the following to work on the repository and use the development server.

## Programs and Applications
1. Python (https://www.python.org/downloads/)
2. Node.js (https://nodejs.org/en/download/)
3. Python virtual environment with install packages:
    ```bash
    # install virtual enviornment with pip
    pip install virtualenv

    # create the virtual environment at project root
    virtualenv venv
    ```

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

### Disabling the PyTorch Model
The PyTorch model takes a lot of processing power and package dependencies, so  to faciliate independent frontend development the flag `USE_ACTUAL_MODEL` has been added. If the value is true, then the actual ML model is imported and used. If false, the random summarizer in the network component is used instead.

The flag is configured in apiutils/configs/summarizer.py, and can be hardcoded to a specific value. However, it is also designed to look for the environment variable `CHATBERTA_NO_MODEL`. If the environment variable exists and its value is `1`, then `USE_ACTUAL_MODEL` will be false. Otherwise, it will be true.

You can set the environment variable on Windows with:

```batch
set CHATBERTA_NO_MODEL=1
```

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