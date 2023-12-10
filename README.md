# tennis
web app for checking DLTC league team eligibility

# Docker Tips
You can create a docker image using the Dockerfile by running the below command from the same folder as where the docker image is saved as that is what the '.' is referring to in the command.
'docker build -t conorwaldron512/summer_league_webapp:1.0 .' where the :1.0 indicates its version 1.0

You can view this image with the command 'docker images'

Note you can have multiple docker files and then specify which one to use to build an image with the -f arugment for filepath 'docker build -f Dockerfile.winter -t conorwaldron512/winter_league_webapp:1.0 .'

You can run the docker image locally (if you have Docker installed and you have created or pulled the image) with the command below. Note that we pick a random port (8888) on the host side but we must use the port 5000 on the container side as that was specified in app.py
'docker run -d -p 8888:5000 conorwaldron512/summer_league_webapp:1.0'
If you then go to localhost:8888 you can see the web app working locally, the same as if you ran app.py from pycharm on your local machine
You can use 'docker ps' to see a list of running containers and you can use 'docker stop <container_id>' to turn off a container
If you encounter any problems you can try to de-bug them by looking at the docker container logs with the command 'docker logs <container_id>'
Note that if you are using any custom modules with a Docker webapp, it is easiest to just put them all in the same directory as the web app and then you can import them without needing a setup.py file or pip installing the module.

###When in doubt, use 'docker logs <container_id>

If you want to see the file system of your docker container when it is running (because you want to try to upload or download files for example) you can use the commands 'docker exec -it <container_id_or_name> ls -l' to do whatever unix command you want, in this case a ls -l. Or you can use 'docker exec -it <container_id_or_name> /bin/bash' to start a terminal directly in that container so you can work away as normal with cd or ls etc.

If you want to publish your docker file to dockerhub you can use 'docker push conorwaldron512/summer_league_webapp:1.0' and then you can see the file on the docker hub wesbite at https://hub.docker.com/
At this point another developer could pull your image, and then run it in a container on their own local machine.

# Deploy docker image to container on cloud
If you want other users to be able to view your webapp without having to run the docker image themselves, then you need to host your image in the cloud.
If you want to do this with AWS elastic bean stalk you need to make a dockerun.aws.json file

# Data requirements
This web app expects the following files in the assets folder
* teams.csv a csv file with the columns Name, Team, Class, Position where Position is S1, S2, S3, D1, D1B, D2 or D2B teams are positive integers like 1, 2, 3
* subs.csv a csv file with the columns Name, Lowest_Class


