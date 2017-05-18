# ras-compose
Developer environment for RAS components. 

This repository is intended to be a single place from which to "check out, build and run" the Respondent Account Services system (RAS). If you have [Docker](https://docker.com/) ([Mac](https://docs.docker.com/#/docker-for-mac) / [Linux](https://docs.docker.com/#/docker-for-linux) / [Windows](https://docs.docker.com/#/docker-for-windows)) and [Docker Compose](https://www.docker.com/products/docker-compose) installed, you *should* be able to clone and go. If it doesn't work for you, do get in touch.

## Overview

The Respondent Account Services application is made up of a collection of repositories. The names of the repositories for this application all start with "ras-". You can find them using a [search for ras repositories](https://github.com/ONSdigital?q=ras-).

In that list, you should see the following components (these may get renamed and the list may change faster than this document):

### Application components

The following components provide the functionality of the Respondent Account Services system:

  * [ras-frontstage](https://github.com/ONSdigital/ras-frontstage) - this is a Python/Flask web application that provides the public user interface to the system.
  * [ras-party](https://github.com/ONSdigital/ras-party) - this is a Python/Flask web application that provides the DB layer between respondents (users), businesses and business surveys
  * [ras-collection-instrument](https://github.com/ONSdigital/ras-collection-instrument) - this is a first iteration of a service to manage survey collection instruments. This is a lightweight best-guess implementation because we'd like to demonstrate building a service that provides some business functionality. It will need to be revisited and iterated as the service develops and evolves.

### Supporting components

The following components are here to capture supporting components:


### Architecture pattern

The following diagram summarises how the components are connected. DB connections are a continuous line:

![Architecture pattern](https://docs.google.com/drawings/d/19qXRtqJwjtz9g6dLOyMWA9W5bXvdiKAuk154g7yCXEk/)

## Running

Here's how to get RAS up and running. For a developer machine, [Docker Compose](https://docs.docker.com/compose/) is a good way to go:

  * To pull and build the set of components, run [./build.sh](https://github.com/ONSdigital/ras-compose/blob/master/build.sh). This will check out each repo and place into a subdirectory of /ras-compose.
  * To start the system, run [./run.sh](https://github.com/ONSdigital/ras-compose/blob/master/run.sh). This will clear down your environment, build container images and start up the components according to the [docker-compose.yml](https://github.com/ONSdigital/ras-compose/blob/master/docker-compose.yml) file.
  * To run things manually if you want to check things out you can do: 1) /> docker-compose down  2) docker-compose build  3) docker-compose up -d
  * To make things a little easier, [ras-frontstage](https://github.com/ONSdigital/ras-frontstage) gets mapped to [localhost:5000](http://localhost:5000) and
  * To get a command-line where you can `curl` individual components, run `./cmd.sh`. You may need to check `docker network ls` to ensure the run script is attempting to attach you to the correct Docker network.

## Developer machine setup

This diagram summarises the kinds of target environment we're looking at for deploying this application. 

![Targetting Cloud Foundry and Docker](https://docs.google.com/drawings/d/1Ch4_BZRWbUSYWQJQF5CsVFU2lu6zFw3okEQjuu3tfks/)

There are basically three ways to get a running system:

  * Build and run each component separately and **manually**. This requires the least amount of supporting infrastructure, but the most manual effort. For a Python Flask system it's /> python app.py for a Python Django project it's /> python manage.py runserver'
  * Run using **Docker Compose**. This should be straightforward and, if you already use Docker, the most straightforward and accessible way of understanding how the components fit together.
  * Run using **Cloud Foundry**. If you like Cloud Foundry, you can run the system using something like [PCF Dev](https://pivotal.io/pcf-dev). This is something of a halfway house. There'll be some manual effort to CF push and configure some of the components, but if CF is a natural environment for you this might be your preferred option.




For a couple of additional resources, see the [/docs](https://github.com/ONSdigital/ras-compose/blob/master/docs) folder in this repo.

There are also specific instructions for setting up [Linux Mint](https://github.com/ONSdigital/ras-compose/blob/master/docs/Linux-Mint.md)


