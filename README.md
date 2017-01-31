# ras-compose
Developer environment for RAS components. 

This repository is intended to be a single place from which to "check out, build and run" the Respondent Account Services system. If you have [Docker](https://docker.com/) ([Mac](https://docs.docker.com/#/docker-for-mac) / [Linux](https://docs.docker.com/#/docker-for-linux) / [Windows](https://docs.docker.com/#/docker-for-windows)) and [Docker Compose](https://www.docker.com/products/docker-compose) installed, you *should* be able to clone and go. If it doesn't work for you, do get in touch.

## Overview

The Respondent Account Services application is made up of a collection of repositories. The names of the repositories for this application all start with "ras-". You can find them using a [search for ras repositories](https://github.com/ONSdigital?q=ras-).

In that list, you should see the following components (these may get renamed and the list may change faster than this document):

### Application components

The following components provide the functionality of the Respondent Account Services system:

  * [ras-frontstage](https://github.com/ONSdigital/ras-frontstage) - this is a Python/Flask web application that provides the public user interface to the system.
  * [ras-respondent](https://github.com/ONSdigital/ras-respondent) - this is a basic Spring Boot microservice to receive calls from the front-end web application.

### Supporting components

The following components are here to provide a Spring Cloud Netflix environment around the application components:

  * [ras-gateway](https://github.com/ONSdigital/ras-gateway) - a Spring Cloud annotation-driven implementation of Zuul.
  * [ras-registry](https://github.com/ONSdigital/ras-registry) - the Spring Cloud single-annotation implementation of Netflix Eureka.
  * [ras-authentication](https://github.com/ONSdigital/ras-authentication) - a forked copy of the [Cloud Foundry UAA component](https://github.com/cloudfoundry/uaa), stripped back to version 3.9.1 because versions 3.9.2 and 3.9.3 fail to start using the Cloud Foundry supplied Quick Start instructions (`./gradlew run`)
  * [ras-config](https://github.com/ONSdigital/ras-config) - the Spring Cloud single-annotation config server. *This is not currently in use as Spring Boot clients don't seem to be able to retrieve their properties from it out-of-the-box, using the Spring-supplied example code*.
  * [ras-config-files](https://github.com/ONSdigital/ras-config-files) - test config properties for [ras-config](https://github.com/ONSdigital/ras-config). *Not currently in use*.
  
### Architecture pattern

The following diagram summarises how the components above form a standard Spring Cloud Netflix environment:

![Architecture pattern](https://docs.google.com/drawings/d/1LBzr-0UqJoLVxNgLoy5dog3O4tihLpVjMvQq6Qs43bU/pub?w=1061&h=719)

## Running

Here's how to get RAS up and running. For a developer machine, [Docker Compose](https://docs.docker.com/compose/) is a good way to go:

  * To pull and build the set of components, run [./build.sh](https://github.com/ONSdigital/ras-compose/blob/master/build.sh). This will check out each repo and, using a Gradle container, compile each Java component.
  * To start the system, run [./run.sh](https://github.com/ONSdigital/ras-compose/blob/master/run.sh). This will clear down your environment, build container images and start up the components according to the [docker-compose.yml](https://github.com/ONSdigital/ras-compose/blob/master/docker-compose.yml) file.
  * To make things a little easier, [ras-frontstage](https://github.com/ONSdigital/ras-frontstage) gets mapped to [localhost:5000](http://localhost:5000) and [ras-gateway](https://github.com/ONSdigital/ras-gateway) gets mapped to [localhost:8080](http://localhost:8080)
  * To get a command-line where you can `curl` individual components, run `./cmd.sh`. You may need to check `docker network ls` to ensure the run script is attempting to attach you to the correct Docker network.

## Developer machine setup

This diagram summarises the kinds of target environment we're looking at for deploying this application. 

![Targetting Cloud Foundry or Docker](https://docs.google.com/drawings/d/1H6k7CheKkCEHCFb91RrQW_XzGEuuXup1ReDwYnBFNJY/pub?w=632&h=387)

There are basically three ways to get a running system:

  * Build and run each component separately and **manually**. This requires the least amount of supporting infrastructure, but the most manual effort.
  * Run using **Docker Compose**. This should be straightforward and, if you already use Docker, the most straightforward and accessible way of understanding how the components fit together.
  * Run using **Cloud Foundry**. If you like Cloud Foundry, you can run the system using something like [PCF Dev](https://pivotal.io/pcf-dev). This is something of a halfway house. There'll be some manual effort to CF push and configure some of the components, but if CF is a natural environment for you this might be your preferred option.

For a couple of additional resources, see the [/docs](https://github.com/ONSdigital/ras-compose/blob/master/docs) folder in this repo.

There are also specific instructions for setting up [Linux Mint](https://github.com/ONSdigital/ras-compose/blob/master/docs/Linux-Mint.md)
