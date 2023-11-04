# picking a base image
FROM python:3.8

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files, folders and files in those folders to the container,
# needed so app has access to previous_week.csv, teams.csv and subs.csv
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# install my own custom made modules, note the './' indicates the tennis folder is in the current working directory
RUN pip install ./tennis

# tell the port number the container should expose
EXPOSE 5000

# run the command, run python and then point at the python script for your app
CMD ["python", "./dashapp/summer_league_app.py"]