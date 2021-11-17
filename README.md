![sample application](output-streamlit.gif)


# Live ISS Tracker

Liveisstracker is a containerized application which tracks and shows the current location of Internation Space Station on an orthographic world plot.
Visit [this](https://share.streamlit.io/manojmanivannan/liveisstracker-streamlit/track_iss.py) interactive page to view the application running on cloud, thanks to Streamlit cloud.

#### Background

A project started as a way to learn how real world projects are developed and deployed into production.
It also serves as a template for creating a python project, build using docker containers, docker-compose and the use of maven. It also includes gitlab continuous integration.

# Make commands

##  Build and Package
This command will build the docker images defined in the docker-compose.yml file, pushes the application image (python), defined in Dockerfile, to gitlab repository
```
make clean package
```

## Run the project
To render maps using mapbox, you need an access token. Follow instructions [here](https://docs.mapbox.com/help/getting-started/access-tokens/). You can use create a free account and get a public access token. Save the public token in your project directory as ```map_secret.txt```. 
This command will run the docker-compose.yml and brings up the application (docker containers) in the background.
```
make clean launch
```
then go to your web browser at ```localhost:8501``` to view the application

## Help
Check other targets using help ```make help```
```
Main targets: LIVE_ISS_TRACKER
clean                   : Clean mvn target folder
stop                    : Stop all containers and bring down docker-compose if up
dk_compose_tests        : Launch the application successfully in docker-compose mode
run_python_tests        : Run python package test. SKIP_REMOVE_CONTAINER=true to skip removing the docker container if tests pass.
run_streamlit           : Runs the Streamlit server on the container.
package                 : Builds docker images and pushes to GITLAB registry
deep_clean              : Cleans mvn target folder, removes docker volumes, containers and images matching 'liveisstracker'
launch                  : Generates resources and brings the docker-compose up 'builds images'
help                    : show this help
```

## Environment setup

### Installation on windows

#### For Maven and Java

Steps followed to install java and maven on a windows machine

1. Download binary zip archive for Maven from [here](https://maven.apache.org/download.cgi)
2. Download Windows compressed archive for Java from [here](https://www.oracle.com/java/technologies/javase-jdk14-downloads.html)
3. Extract both in ```C:\dev\tools``` in their own folders
4. Add system variables
    1. ```JAVA_HOME``` pointing to folder ```C:\dev\tools\jdk-folder```
    2. ```MAVEN_HOME``` pointing to folder ```C:\dev\tools\maven-folder```
5. Edit system variable 'PATH'. Add two new entries ```%JAVA_HOME%\bin``` and ```%MAVEN_HOME%\bin```

verify java by opening new command prompt and typing ```java --version``` and ```mvn --version``` for maven

#### For Docker

Install docker cli from [here](https://docs.docker.com/toolbox/toolbox_install_windows/)

#### For Make

```make``` is a GNU command so the only way you can get it on Windows is installing a Windows version like the one provided by [GNUWin32](http://gnuwin32.sourceforge.net/packages/make.htm). Or you can install [MinGW](http://www.mingw.org/) and then do: ```copy c:\MinGW\bin\mingw32-make.exe c:\MinGW\bin\make.exe```. Then update the PATH to include the bin directory of the make.exe.

### Installation on Linux

Java and Maven can be setup by installing maven alone, which will pull its java dependency

```sudo apt-get install maven``` for debian/ubuntu

## CLI Release 

This project also generates a command line utility that can be installed from https://pypi.org/project/liveisstracker/ .

```pip install liveisstracker```

```
  Usage: liveisstracker [OPTIONS]

  liveisstracker can get location,speed and pass-over country based on
  current location of International Space Station

  Options:
  -i, --get-iss-location       Get the current location of International Space
                                  Station + Google MAP URL
  -s, --get-iss-speed          Get the current ground speed of International
                                  Space Station
  -c, --get-country            Get the country above which the ISS is current
                                  passing over
  -p, --plot-iss FILENAME.png  Plot the current position of International
                                  Space Station on a map
  -h, --help                   Show this message and exit.
```

```
$ liveisstracker -i -s
Timestamp (UTC): 2021-11-17 15:52:05 ISS is at Lat:24.6399 Lon:30.1919
https://maps.google.com/?q=24.6399,30.1919&ll=24.6399,30.1919&z=3
Ground Speed of International Space Station is ~ 24833.19 Km/h
```
