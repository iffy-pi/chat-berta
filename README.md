# Chat-Berta
Chat-Berta Project File.

This also serves as the repository for ELEC498 Group 12 (JISH)

## Directory Information:
This entire repository is used to package the web application for Chat-Berta. This means most of the files here are all useful for the web server.

deploy-web-server.md contains information on how to deploy the web server (during its initial creation) and is archived as a good source of informaiton.

git-pr.bat is a simple batch script that streamlinees the opening of pull requests for the application.

server-void/ contains files and folders that are not relevant to the web server. That is the web server can be deployed without the files in this folder. **All files required by the server can NEVER be put in server-void/**

# Development Pipeline
## Standard Commits (No Web App Deployments)
This is the case where there are no deployments to the Vercel web app, i.e. standard changes to the repository. This can be handled by making pushes to the main branch of the repo (i.e. `main`), however as there are multiple people working on things, extensive changes should be handled in separate branches and then merged with the main branch.

Remember to work in the virtual environment using:
```
venv\Scripts\activate.bat
```

### Pull Latest Changes from mainline
Switch to mainline branch if you are not on there already:
```
git checkout main
```
Then pull
```
git pull
```

### Create Developmental Branch (if applicable)
Use a development branch if you are doing extensive changes. Create a new development branch of the current branch (main) with a name in the format: `<dev>-<user>-<description>` e.g.
```
git checkout -b dev-iffy-sample-dev-branch
```

Branches allow you to continue experimental work without interfering with the working code in mainline.

### Make your changes adn commits
Note that whenever you install new packages, be sure to reupdate the requirements file with:
```
pip freeze > requirements.txt
```
You can test changes by using the developmental server:
```
python app.py
```

Commit changes to your branch if you created one, or the main branch as follows.

### Push Branch
Push all your commits by using the command:
```
git push
```
Note: You can make more commits and push as usual until you are ready to merge with the main branch.

### Merge With Main (if you created a developmental branch)
Merge your branch with the mainline by initiating a pull request, this can be done using the added utility git-pr.bat:
```
git-pr.bat
```
Enter `Y` to open a pull request and make sure to select `main` as the branch to merge with.
Ideally, we should review merges to the mainline, but this may not be guaranteed.

## Web App Deployments
In this case, we deploy contents from the `main` branch to the Vercel app, this can be done by merging the contents of the `main` branch, to `vercel-production`