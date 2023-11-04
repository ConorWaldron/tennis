# tennis
web app for checking DLTC league team eligibility

# Docker Tips
You can create a docker image using the Dockerfile by running the below command from the same folder as where the docker image is saved as that is what the '.' is referring to in the command.
'docker build -t conorwaldron512/summer_league_webapp:1.0 .' where the :1.0 indicates its version 1.0

You can view this image with the command 'docker images'

You can run the docker image locally (if you have Docker installed and you have created or pulled the image) with the command below. Note that we pick a random port (8888) on the host side but we must use the port 5000 on the container side as that was specified in app.py
'docker run -d -p 8888:5000 conorwaldron512/summer_league_webapp:1.0'
If you then go to localhost:8888 you can see the web app working locally, the same as if you ran app.py from pycharm on your local machine
You can use 'docker ps' to see a list of running containers and you can use 'docker stop <container_id>' to turn off a container

If you encounter any problems you can try to de-bug them by looking at the docker container logs with the command 'docker logs <container_id>'

Note that if you are using any custom modules in Docker, the setup.py for those files needs to be inside that folder... like below

- Dockerfile
- tennis/
  - setup.py
  - other_module_files.py


# Data requirements
This web app expects the following files in the assets folder
* teams.csv a csv file with the columns Name, Team, Class, Position where Position is S1, S2, S3, D1, D1B, D2 or D2B teams are positive integers like 1, 2, 3
* subs.csv a csv file with the columns Name, Lowest_Class


