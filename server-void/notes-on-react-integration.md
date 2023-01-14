# Steps To Migrate Vercel Deployment from Flask to React
1. Install react app directly to Chat-Berta repo by doing `npx create-react-app Chat-Berta`

2. Connect the flask backend to the react frontend by adding the proxy key to the json


# Other Other Notes for steps
First I did testing with the local react and flask servers and got the json responses working.

Then I tried to do it in deployment but it failed, it seems that I have to host the front end and the backend separately, this will be done by hosting them separately on vercel

First I took our current deployment (chat-berta) and changed it to match chat-berta-api, that way it will be for the flask backend

Then I also changed the project settings to now sync to the api-vercel-production, this will be our backend page.

Next I created the branch `app-vercel-production` for deploying the react app.

On the local server, I first created the react app in the correct folder (had to change the local repository name from `Chat-Berta` to `chat-berta`)

Then in the root directory I created the react app, copied over the src folder from here and tested it in the development (also copied proxy)

Once I worked that out, I went and created a project in Vercel chat-berta and set the framework to react!

I set the branch to app-vercel-production.

The current issue, is that vercel.json conflicts with the app deployment, and deleting conflicts with the api deployment:

The fix:
- Keep the json present in the main branch, and then add a deletion commit to the app-vercel-production branch and  note it in the readme

Possible fix, override build instruction manually in chatberta api?



# Other Notes
Change flask run port by setting the env variable `FLASK_RUN_PORT` to the port number of your choice

Fixed proxy error by changing `localhost` to `127.0.0.1` in the proxy value mapping