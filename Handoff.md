# Handoff Instructions

## Local Development

See [README.md](README.md) for setup instructions on your local machine.

## Manual Deployment

### Introduction

We use Docker to build and package the project. This means that it should be able to run on any server running almost any operating system. Thus, you can deploy it on your own server, using a Virtual Machine in a public cloud service like AWS or Google Cloud, or using a fully-managed cloud service for Docker containers, such as Google Cloud Run.

You can use either build and deploy the Docker image manually or a CI/CD service like GitHub Actions to build and deploy the Docker image.

### Building the Project

#### Backend

To build the Docker image, first make sure you have [Docker](https://docs.docker.com/engine/install/) and Git installed on the server you are deploying to.

Next, clone this Git repository and navigate to it in the terminal. Build the Docker image using

```[sh]
docker build -t backend:latest --build-arg FRONTEND_URL={frontend URL} --build-arg BACKEND_URL={backend URL} .
```

Make sure to replace `{frontend URL}` and `{backend URL}` with the correct values for deployment.

You can also add `--build-arg SUPERUSER_EMAIL={email}` and `--build-arg DJANGO_SUPERUSER_PASSWORD={password}` to change the initial admin credentials. (By default they are `admin@example.com` and `admin`) Otherwise you can change them after deployment.

(Note: you may need to use `sudo` in front of `docker` commands on some Linux systems.)

The build process will take a couple of minutes, but after it is done you can verify by running `docker images`.

#### Frontend

Now we build the frontend. We are not using a Docker image for this since it would be cost-ineffective, as the frontend files are static JavaScript. We used Firebase Hosting to host the frontend, but there are some other services out there such as CDNs.

Make sure you have `npm` installed on your local machine.

Run `npm install` to install the dependencies of the project and then run `npm run build` to build a production version.

Now we can deploy these files to our hosting provider.

For Firebase, follow [these instructions](https://firebase.google.com/docs/hosting/quickstart) to set up Firebase and deploy your project.

You will probably need to remove the current `.firebaserc` and `firebase.json` files first so that the Firebase CLI does not get confused.

The react frontend has environment variables that can be changed located in .env. These will work for the project as it is now, however may need to be changed for future iterations or for testing.

REACT_APP_BACKEND_URL determines the URL used when not running the server locally (through npm start). This is the url which will be accessed when deployed to firebase.
REACT_APP_USE_BACKEND_URL is set to false. If set to true then the REACT_APP_BACKEND_URL will always be used even on the locally run server, which may be useful for testing purposes during url setup.
REACT_APP_DEFAULT_PORT determines the port number when the server is run locally. 

### Running the Project

Now, just like for local development, you can run the backend on the server using:

```[sh]
docker run -e "PORT=8080" -p 8080:8080 backend
```

you can run on a different port by simply replacing the number 8080 above with the port number you'd like to use.

If you deployed to a service like Firebase in the previous step, then the frontend should already be running.

## Automated Deployment

### Introduction

We used GitHub Actions for our CI/CD, but there are other tools such as Travis or CircleCI that will work similarly.

The GitHub Actions scripts are set up in the `.github/workflows/` directory, and you should reference them throughout this guide.

This guide will walk you through how to set up automated deployment using Google Cloud Run for the backend and Firebase Hosting for the frontend.

### Backend

First you will need to set up a project in Google Cloud.

Next, follow [these instructions](https://github.com/marketplace/actions/deploy-to-cloud-run) to configure the Service Account needed to run the workflow. You'll need to add the JSON Service Account key to the Repository Secrets in GitHub (in `deploy_backend.yml`, this is referenced as `GCP_SA_KEY`). You should also add the project name as `GCP_PROJECT`.

This "Build and Push Container" step builds the Docker container on GitHub Actions and pushes it to Google Container Registry. Then, the "Deploy to Cloud Run" step simply tells Google Cloud Run to deploy the image from Container Registry.

You may need to modify some parts of `deploy_backend.yml` depending on your Google Cloud configuration. For example, `SERVICE` (the image name), `REGION`, and `build_extra_args` in the "Build and Push Container" step might change depending on how/where you wish to deploy the app.

### Frontend

Make sure you have created a Firebase project at [https://firebase.google.com/](https://firebase.google.com/).

The `deploy_frontend.yml` workflow file can be mostly generated automatically using the Firebase CLI: simply run `firebase init hosting` and the tool will walk you through setting up GitHub Actions to automatically deploy the frontend.

At the end, you will get a new `.yml` file which you can use as a template (along with the current `deploy-frontend.yml`).

## Automated Testing

We also use GitHub Actions to run automated unit tests on the Django app (see `backend-tests.yml`).

The Python dependencies are cached between runs to avoid reinstalling the same libraries every time, so the workflow runs are fairly time-efficient (running in less than a minute).
