*** READ ME ***

Make sure you are in a Python 2 environment (e.g. conda or virtualenv).


Use Terminal to enter this directory and type the following
to start gcloud serving your app on localhost:8080:

    dev_appserver.py .


You can deploy your app to the cloud so anyone in the world can view it with the following command:

    gcloud app deploy

This will deploy your 'default' project in the current configuration.
Once deployed, your app will be available to view and use at the address

    http://[YOUR_PROJECT_ID].appspot.com .

Or issue the command:

    gcloud app browse

which will open up your default browser to the public URL for the project.
This may not work though, depending on your configuration.


Include the --project flag to specify an alternate GCP project ID to what you initialized as the default in the gcloud tool:

    gcloud app deploy --project [YOUR_PROJECT_ID]


other useful commands:
list configurations:        gcloud config configurations list
list projects:              gcloud projects list
change default project:     gcloud config set project [YOUR_PROJECT_ID]


This project is live at the following url:
https://sudoku-solver-190907.appspot.com
