# Silicon_Artists

## Description

We are building a website with a backend for the Toronto Police Services Board to allow administrators to record meeting information/minutes and display the information and agendas of these meetings to the general public. The website will help make Board meetings more accessible to the general public in Toronto interested in being engaged with oversight of the Toronto Police Service Users: Board Administrator / Board Members. The website will also allow for more straightforward modification and recording of information directly related to tpsb meetings, to assist board admisistrators.

Currently the partner is using a 300-page long PDF to record this information and modifying it using Joomla CMS. This process is labour intensive and not very accessible to the public. The product will allow for all the information to be displayed clearly and for administrators to update and add to the information easily.

## Key Features

The key features that are currently accessible to the user are the ability to create, delete, edit and modify meetings, and their respective meeting agendas, agenda items and minutes on the admin site, accessible only to the administrator behind username/password. The other main feature is that the information in these are accessible to everyone through the main website, where one can observe any created meeting’s information, reading the agenda or minute information, all displayed there.
Meetings represent a given tpsb meeting, having a date, title, and optionally an agenda, a youtube link to a recording of the meeting and/or a minutes document.

Each agenda has an agenda item for each proposal or proposition planned to be discussed in the meeting, and there is only at most one agenda in each meeting. The agenda items have rich text editing options, and are numbered. Each agenda item also can have an attachment, such as a powerpoint or image for relevant proposal or discussion, motions carried forth upon the item, and result status of the proposal.
Each minute has rich text, and would theoretically have records and times of the completion and decision result on items in the Agenda.

These are all displayed on the publicly accessible frontend.

## Instructions

The admin site can be accessed at [https://backend-smtcuvoqba-uc.a.run.app](https://backend-smtcuvoqba-uc.a.run.app) and the frontend site can be accessed at [https://tpsb-330016.web.app](https://tpsb-330016.web.app).
The admin site has a pre-created account, a superuser, and that user may create additional users.

Credentials for admin site are: Username: `admin`, password: `admin`

The admin website has option to create new or edit existing meetings, agendas and meetings, done by clicking on the plus to the right of the item names along the left. (There is also an option in the top right after selecting one them) It is where all changes to the database and backend are sent from.

One can also view all sets of items. Agenda items are all visible and addable when selecting an Agenda, as all Agenda items belong to a particular Agenda.

![admin-site](/deliverable-2/images/django-backend.png)

The changes there are all visible on the frontend website. All meetings are displayed in order of most recent date. Clicking on a meeting displays a box below where one may read the agenda or meeting information dictated in the admin site. Attachments are downloadable from the frontend, however they do not display there at the moment.

With out current cloud database, all information is stored temporarily on the free tier. So after about 30 minutes of inactivity the information will be deleted. This will be resolved by deliverable 3.

## Development requirements

*Languages: Python 3.9 (Pipenv) and Node 12 (npm).*

There are two ways to run the backend locally:

### Option 1: Manual setup

- To set up the Python backend’s dependencies, we are using Pipenv (install using `pip install pipenv` or `pip3 install pipenv`). To install the dependencies, navigate to the project directory and run `pipenv install`. Note that the dependencies are listed in the `Pipfile` and their versions in the `Pipfile.lock`.
- To activate the virtual environment, run `pipenv shell`.
- Set up the database using `python manage.py makemigrations` and `python manage.py migrate`.
- Create a new user with `python manage.py createsuperuser` which will prompt you for credentials.
- Run the development server using `python manage.py runserver`.

### Option 2: Docker

Make sure you have Docker installed on your machine.

- Build the docker image using `docker build -t backend .` (you may need `sudo` if you are on Linux)
- Run the docker image using `docker run -e "PORT=8080" -p 8080:8080 backend` (again, you may need `sudo`). You can use whichever port you’d like.

### Frontend

For the frontend, you will need `npm`.

- To install the dependencies, run `npm install`.
- You can run the frontend using `npm start`.
- To produce a minified build for deployment, use `npm run build`.

## Deployment and Github Workflow

We use a Git feature workflow with a `develop` branch. Thus, the `master` branch represents the code that has been deployed to the demo server, the `develop` branch represents ongoing work on the project, and other feature branches are created from `develop`. A pull request will start from a feature branch and is reviewed by at least one other group member before being merged into `develop`. Once the group is satisfied with the state of a project, we create a pull request and at least three members review it before it goes into `master`.

Note that on every push to every branch, we use GitHub Actions to run automated unit testing of the application.

We chose this Git workflow because our application has several different components and features which need to be worked on at the same time. This way, everyone can work on their own component and we can easily merge them together and deploy the application.

For deployment, we use automation through GitHub Actions. The backend is deployed using a workflow that builds a Docker image using the Dockerfile, uploads it to Google Container Registry, and deploys it to Google Cloud Run where it is publicly accessible. The frontend is deployed using a different workflow which creates a minified production build of the React app (using `npm run build`) and deploys it to Firebase Hosting where it is also publicly accessible. The credentials for Google Cloud and Firebase are stored in the Repository Secrets in GitHub.

For all of our GitHub Actions workflows, we made sure to implement caching of the dependencies/libraries and build artifacts so that subsequent runs of the workflows would be much faster. This way, we do not waste Actions time.

We decided to use severless platforms for deployment like Google Cloud Run and Firebase in order to simplify deployment and the eventual handoff to our partner. This way, we do not have to manage server infrastructure such as VMs, and because we are testing our code with low volume, we easily fall into the free tier of GCP.

## Licenses

We are using the MIT license for the codebase. Therefore, anyone has the ability to reuse the code, provided they include the same notice in their derivative work. Our partner is okay with any open-source license, since they are interested in sharing the code with other police departments, so we decided to use a very permissive one to keep everyone’s options open in the future.
