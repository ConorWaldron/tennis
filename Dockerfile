# picking a base image
FROM python:3.8

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files, folders and files in those folders to the container,
# needed so app has access to previous_week.csv, teams.csv and subs.csv
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# tell the port number the container should expose
EXPOSE 5000

# Set the working directory to the app folder, this will ensure relative paths work in the same way as if you clicked run on app.py
WORKDIR /usr/src/app/dashapp

# run the command, run python and then point at the python script for your app
CMD ["python", "./summer_league_app.py"]