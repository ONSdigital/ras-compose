# ras-compose
Developer environment for RAS components.

## Overview

The Respondent Account Services application is made up of a collection of repositories, starting with "ras-". You can find them using a [search for ras repositories](https://github.com/ONSdigital?q=ras-).

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

## Developer machine setup

The following is a how To guide for getting a dev environment up For ubuntu 16.04 or derivative (e.g. Mint 18)


### Preamble

This guide is written after trial on Linux Mint 18, hence may have text fields in example related to this.
Linux Mint 18 is a derivative of Ubuntu 16.04, all commands should work.

### Introduction

This guide should step you through the steps needed to get a default Linux distro to the point where you can
spin up docker containers on your machine. Each container will pull down the relevant source code to run the
application software for each service.
Each container will map to a Pivital [CloudFoundary Microservice](https://content.pivotal.io/microservices),
with the exception of a python web app using the python Flask micro service.

### Software Components Recommended

Recommended is Pythons Virtual Environment Wrapper. This makes setting up Python Virtual Environments easy!
Ansible 2.1.0.0, which will help in orchestration.

### Software Components Needed

To run the spring boost micro services you will need a Java Virtual Machine and the SDK, with openjdk version
"1.8.0_111", OpenJDK 64-Bit Server VM.
Python 2.7 is used for the Flask micro service but this is will be installed as standard, joy!
A Python virtual environment package is needed version 15.0.1.
Docker (Docker Engine version 1.13.0, Docker Machine version 0.8.2 and Docker Compose  version 1.8.1)
Gradle 3.3 the Java package manager.


### Setting Up Java

Versions of Java Needed are Java 8. Which equates to Java Development Kit (JDK) & Jave Runtime Environment (JRE1.8).
On my machine I'm using Open JDK 8. Use the package managers version. If you get any errors due to Error 404 with your
package manager not finding a repo it might mean you need to purge your apt repos and update your packages index:

	/> sudo apt-get install openjdk-8-jre
	/> sudo apt-get install openjdk-8-jdk

If there are any errors in running this that relate to broken index's, 404 errors, or broken dependencies it might be
that your package manager index is out of date. e.g.


		Reading package lists... Done
		Building dependency tree
		Reading state information... Done
		Correcting dependencies... Done
		The following additional packages will be installed:
		  openjdk-8-jdk openjdk-8-jdk-headless
		Suggested packages:
		  openjdk-8-demo openjdk-8-source visualvm
		Recommended packages:
		  libxt-dev
		The following NEW packages will be installed
		  openjdk-8-jdk openjdk-8-jdk-headless
		0 to upgrade, 2 to newly install, 0 to remove and 0 not to upgrade.
		2 not fully installed or removed.
		Need to get 8,618 kB of archives.
		After this operation, 39.7 MB of additional disk space will be used.
		Do you want to continue? [Y/n] y
		Err:1 http://security.ubuntu.com/ubuntu xenial-security/main amd64 openjdk-8-jdk-headless amd64 8u111-b14-2ubuntu0.16.04.2
		  404  Not Found [IP: 91.189.88.152 80]
		Ign:2 http://security.ubuntu.com/ubuntu xenial-security/main amd64 openjdk-8-jdk amd64 8u111-b14-2ubuntu0.16.04.2
		Err:1 http://security.ubuntu.com/ubuntu xenial-security/main amd64 openjdk-8-jdk-headless amd64 8u111-b14-2ubuntu0.16.04.2
		  404  Not Found [IP: 91.189.88.152 80]
		Err:2 http://security.ubuntu.com/ubuntu xenial-security/main amd64 openjdk-8-jdk amd64 8u111-b14-2ubuntu0.16.04.2
		  404  Not Found [IP: 91.189.88.152 80]
		E: Failed to fetch http://security.ubuntu.com/ubuntu/pool/main/o/openjdk-8/openjdk-8-jdk-headless_8u111-b14-2ubuntu0.16.04.2_amd64.deb  404  Not Found [IP: 91.189.88.152 80]

		E: Failed to fetch http://security.ubuntu.com/ubuntu/pool/main/o/openjdk-8/openjdk-8-jdk_8u111-b14-2ubuntu0.16.04.2_amd64.deb  404  Not Found [IP: 91.189.88.152 80]


To get a new index refreshed you can do the following:

	/> sudo apt-get update
	/> sudo apt-get clean
	/> sudo apt-get autoremove
	/> sudo apt-get -f install

Now you should be able to get the JDK installed. :-)

	/> sudo apt-get install openjdk-8-jdk

To test you have the correct version do:

	/> java -version
	java -version
	openjdk version "1.8.0_111"
	OpenJDK Runtime Environment (build 1.8.0_111-8u111-b14-2ubuntu0.16.04.2-b14)
	OpenJDK 64-Bit Server VM (build 25.111-b14, mixed mode)


### Setting Up VirtualEnv and VirtualEnvWrapper

Virtualenv is a tool used to allow a developer to create 'software containers' for Python. What this means is that
the developer can produce a python application that is targeted to and built with a set version of Python and all the
sub-component libraries that may be needed. It does not mean a virtual machine or even a container such as docker.
I've included 'VirtualEnvWrapper' which is a wrapper over virtualenv that allows you to easily work with your python
software 'containers'.

1) Use the software package managers version of virtualenv. Do not use the 'pip install' method!

/> sudo apt-get virtualenv

Now use the python package manager to get virtualenvwrapper

/> sudo pip install virtualenvwrapper

2) Setup your bashrc script to provide environment variables for virtualenve

		# Added by Nicholas Herriot 25/01/2017 to get virtualenvwrapper working properly.
		# See: https://virtualenvwrapper.readthedocs.io/en/latest/

		# My machine has virtual environments here.
		#export WORKON_HOME=$HOME/virtalenv
		export WORKON_HOME=/home/nherriot/virtalenv

		# Where projects will reside. I have my projects also in my virtual environment
		#export PROJECT_HOME=$HOME/virtalenv
		export PROJECT_HOME=/home/nherriot/virtalenv

		# I've gone for a generic virtualenvwrapper and not down to individual user so my virtualenvwrapper
		# lives in here. If you have gone through the 'user' route you would have put it here:
		# source $HOME/.local/bin/virtualenvwrapper.sh

		source /usr/local/bin/virtualenvwrapper.sh

3) Setup your profile script to populate your environment path with the virtualenvwrapper. Your profile should look
something like this:


	# set PATH so it includes user's private bin if it exists
	if [ -d "$HOME/bin" ] ; then
		PATH="$HOME/bin:$PATH:$HOME/virtalenv:$GRADLE_HOME/bin"
	fi


### Setting Up Docker

Docker is needed to run the microservice in isolated containers (there are lots of them!) We could use VM's, Vagrant and
ansible - however the environment needed to support multiple (6 minimum) servers each with a micro service is not
feasible. A Docker container is based on a chroot environment and hence does not need the machine resources to run
that a virtual machine would. More info on Docker can be [found here](https://www.docker.com/what-docker)

On your system you will need 3 docker components running on your machine each documented below

#### Docker and Docker Engine
Docker is the main application which allows a user to run docker. Docker version required is 1.13.0. Do not
update your apt package index, it will not be recent enough. Download the latest version by adding the
docker package index:

1) Update your package manager first

	/> sudo apt-get update


2) Download needed extensions to your machine that you may need. This ensures you have 'curl' and Linux
kernel extensions:

	/> sudo apt-get install curl linux-image-extra-$(uname -r) linux-image-extra-virtual

3) Add the security keys and package repo needed to get the latest version:

	/> sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
	/> sudo apt-add-repository 'deb https://apt.dockerproject.org/repo ubuntu-xenial main'

4) Update your package manager to include the new packages

	/> sudo apt-get update

5) Now use the package from this repo and not your default. To ensure this is the case you can do:

	/> apt-cache policy docker-engine

	docker-engine:
	  Installed: 1.13.0-0~ubuntu-xenial
	  Candidate: 1.13.0-0~ubuntu-xenial
	  Version table:
	 *** 1.13.0-0~ubuntu-xenial 500
	        500 https://apt.dockerproject.org/repo ubuntu-xenial/main amd64 Packages
	        100 /var/lib/dpkg/status
	     1.12.6-0~ubuntu-xenial 500
	        500 https://apt.dockerproject.org/repo ubuntu-xenial/main amd64 Packages
	     1.12.5-0~ubuntu-xenial 500
	        500 https://apt.dockerproject.org/repo ubuntu-xenial/main amd64 Packages
	     1.12.4-0~ubuntu-xenial 500
	        500 https://apt.dockerproject.org/repo ubuntu-xenial/main amd64 Packages
	     1.12.3-0~xenial 500
	        500 https://apt.dockerproject.org/repo ubuntu-xenial/main amd64 Packages
	     1.12.2-0~xenial 500
	        500 https://apt.dockerproject.org/repo ubuntu-xenial/main amd64 Packages
	     1.12.1-0~xenial 500
	        500 https://apt.dockerproject.org/repo ubuntu-xenial/main amd64 Packages
	     1.12.0-0~xenial 500
	        500 https://apt.dockerproject.org/repo ubuntu-xenial/main amd64 Packages
	     1.11.2-0~xenial 500
	        500 https://apt.dockerproject.org/repo ubuntu-xenial/main amd64 Packages
	     1.11.1-0~xenial 500
	        500 https://apt.dockerproject.org/repo ubuntu-xenial/main amd64 Packages
	     1.11.0-0~xenial 500
	        500 https://apt.dockerproject.org/repo ubuntu-xenial/main amd64 Packages

Note that it's not installed, so now to install it do:

	/> sudo apt-get install -y docker-engine

You can check that it's working by doing, which shows output from my machine:

	/> sudo systemctl status docker

[sudo] password for nherriot:
● docker.service - Docker Application Container Engine
   Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2017-01-25 11:41:02 GMT; 4h 46min ago
     Docs: https://docs.docker.com
 Main PID: 1168 (dockerd)
    Tasks: 33
   Memory: 61.6M
      CPU: 1min 16.689s
   CGroup: /system.slice/docker.service
           ├─ 1168 /usr/bin/dockerd -H fd://
           ├─ 1535 docker-containerd -l unix:///var/run/docker/libcontainerd/docker-containerd.sock --metrics-interval=0 --start-timeout 2m --stat
           └─14505 docker-containerd-shim e34acd23c8cddb206441791a3b01af3aa777318f97f3527c60487befdfa4621c /var/run/docker/libcontainerd/e34acd23c


You will be able to get more detailed information from the following resources if things go wrong. This guide
is a mix from those resources:

[resource 1](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04)
[resource 2](https://docs.docker.com/engine/installation/linux/ubuntu/)


#### Docker Machine
Docker engine allows you to interface with and control multiple containers that can be running remotely in the
machine. The version required is 0.8.2. This will be a manual installation.
1) Fist create a directory to
contain your 3rd party packages that are not part of your package manager. Once you have done this create a
sub directory to contain your docker machine binary.

	/> mkdir docker-machine
	/> cd docker-machine/

2) Download a version of docker machine that is needed for your particular architecture. Then move it to your
usr local bin folder.

	/> wget https://github.com/docker/machine/releases/download/v0.8.2/docker-machine-$(uname -s)-$(uname -m)
	/> sudo mv docker-machine-Linux-x86_64 /usr/local/bin/docker-machine

3) You can check your version of docker machine with the command line.

	/> docker-machine -version
	/> docker-machine version 0.8.2, build e18a919

#### Docker Container
The Docker Container app is used for running scripts that control (i.e. start, stop, build and create) containers.
It's an orchestration layer based on the open source 'fig' project. The version required is 1.8.1. First lets
download it directly to our /usr/local/bin directory for our particular machine architecture:

	/> sudo curl -o /usr/local/bin/docker-compose -L "https://github.com/docker/compose/releases/download/1.8.1/docker-compose-$(uname -s)-$(uname -m)"

You can use wget and a mv command if you wish, I just used this out of convenience and can't be bothered
changing the one above.




### Setting Up Gradle

Gradle is a package/build manager for Java. It's based on Ant and Groove. You don't need to install Groovy as it's
included in the package. You are not able to use the package managers version - which is at 2.1. We need to use version
3.3. You can find out [details on Gradle here](https://docs.gradle.org/current/userguide/installation.html).

1) First go to your directory setup for 3rd party packages that are outside the version packaged with your system.

	/> cd <your 3rd party pacakges directory>
	/> wget https://services.gradle.org/distributions/gradle-3.3-bin.zip
	/> unzip unzip gradle-3.3-bin.zip

This will place your gradle installation into a folder called 'gradle-3.3'. Next we need to create an environment
variable and add the new binary to our path. I would recommend that you **DO NOT** simply add the binary to /usr/bin
directory keep that save.

2) Add the gradle environment variable to your bashrc script using your favourite text editor, I'm using geany.

	/> cd ~
	/> geany .bashrc

Add the equivalent to your script at the end:

	# Added by Nicholas Herriot 25/01/2017 to get my environment using gradle 3.3 and not
	# the package managers verion
	export GRADLE_HOME=/home/nherriot/virtalenv/ONS-ras/needed-packages/gradle-3.3/bin

3) In your profile script add the **GRADLE_HOME** directory to your path

	/> cd ~
	/> geany .profile

Add the equivalent to your script where gradle is addded to your path string.

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH:$HOME/virtalenv:$GRADLE_HOME"
fi

4) Nothing will have changed unless you re-run the bash scripts. Testing your gradle version shows:

	/> gradle -version


	nherriot@Zenbook-UX32A ~ $ gradle -version
	------------------------------------------------------------
	Gradle 2.10
	------------------------------------------------------------

Now we need to manually run those scripts in our shell to test.

	/> source .bashrc
	/> source .profile

	/> echo $PATH
	/home/nherriot/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/home/nherriot/virtalenv
	/> echo $PATH
	/home/nherriot/bin:/home/nherriot/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/home/nherriot/virtalenv:/home/nherriot/virtalenv:/home/nherriot/virtalenv/ONS-ras/needed-packages/gradle-3.3/bin

Or simply restart your machine! :-)



### Testing Docker Works

This section will ensure that you have all your docker components working without googling for 2 hours trying to
find good guides. Starts with the basics and ensures you are up to speed in no time! Remember a docker container is
'like' a VM - or for me I like to think that it can be thought of as a mini VM, without the need to virtualise the
whole hardware stack. Docker runs on 'ring 0' meaning that it is not truly an insulated environment and will be open
to kernel exploits.

1) First check to see if you have any docker images. An image is a recipe to get an installed system with the
components you want (e.g. a postgres image will have all the postgres components you need to start using.)

nherriot@Zenbook-UX32A ~/scratch/docker $ sudo docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
composetest_web     latest              27df04ea64e1        54 minutes ago      93.4 MB
<none>              <none>              f9ba25fa78ae        18 hours ago        643 MB
frekele/gradle      latest              9313192f62ee        4 days ago          625 MB
ubuntu              latest              f49eec89601e        5 days ago          129 MB
python              3.4-alpine          765c483d587c        5 days ago          82.4 MB
nginx               latest              a39777a1a4a6        8 days ago          182 MB
openjdk             latest              d23bdf5b1b1b        9 days ago          643 MB
hello-world         latest              48b5124b2768        12 days ago         1.84 kB
redis               alpine              53df695896ac        3 weeks ago         19.8 MB

This shows multiple images on my machine.

2) To download an image with docker from [docker hub](https://hub.docker.com/) you can search and download by:

nherriot@Zenbook-UX32A ~ $ sudo docker search ubuntu
NAME                              DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
ubuntu                            Ubuntu is a Debian-based Linux operating s...   5432      [OK]
ubuntu-upstart                    Upstart is an event-based replacement for ...   69        [OK]
rastasheep/ubuntu-sshd            Dockerized SSH service, built on top of of...   66                   [OK]
consol/ubuntu-xfce-vnc            Ubuntu container with "headless" VNC sessi...   39                   [OK]
to............
.............. etc

docker pull ubuntu:12.04
12.04: Pulling from library/ubuntu
ca7b5b0830b2: Pull complete
c49a5127e973: Pull complete
b4663c774444: Pull complete
197fb8a137ca: Pull complete
37caad81dc9f: Pull complete
Digest: sha256:abdc090336ba4503bd72d0961a4f3d45134900d9a793d3f0c06a64d2555fbab7
Status: Downloaded newer image for ubuntu:12.04


3) Run the docker hello_world which will download this image and run it in a container.

	nherriot@Zenbook-UX32A ~/scratch/docker $ sudo docker run hello-world
	[sudo] password for nherriot:

	Hello from Docker!
	This message shows that your installation appears to be working correctly.

	To generate this message, Docker took the following steps:
	 1. The Docker client contacted the Docker daemon.
	 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
	 3. The Docker daemon created a new container from that image which runs the
	    executable that produces the output you are currently reading.
	 4. The Docker daemon streamed that output to the Docker client, which sent it
	    to your terminal.

	To try something more ambitious, you can run an Ubuntu container with:
	 $ docker run -it ubuntu bash

	Share images, automate workflows, and more with a free Docker ID:
	 https://cloud.docker.com/

	For more examples and ideas, visit:
	 https://docs.docker.com/engine/userguide/

You will be presented with a screen like above. This shows all major components are working.

4) Last part in using plane docker is to run a docker container, the command line arguments are
/> docker run <image_name>/<tag_name>. If you miss out the tag name you will get the latest version. See more
information on the [docker run parameters](https://docs.docker.com/engine/reference/run/)

	/> sudo docker run ubuntu

 Nothing much happens here! The container runs but returns immediately. This is because the containers root process
 runs. Does nothing and then returns from it's detached mode. To get something meaningful you need to attach to the
 detached process, and provide the container with a command to run that will return something. First we need to allocate
 a sudo tty input/output process to the container (t flag) and keep STDIN/STDOUT open (i flag). Lastly we need to run
 the bash command in our container. This would look like:

	/> sudo docker run -i -t ubuntu bash

or a more compact version is:

	/> sudo docker run -it ubuntu bash
	root@6393dd967703:/#

To find out what the flags are you can [see this page](https://docs.docker.com/engine/reference/run/). You will notice
that you can list, use top, or do anything inside a bash terminal. To exit this container you would just type 'exit'
as you would in a normal terminal.

5) Stopping and removing a container. To stop the container find out the image name (using /> sudo docker ps)
 and use the stop command:


	/> sudo docker stop modest_noyce
	/> modest_noyce

Then remove the image:

	/> sudo docker rmi modest_noyce




### Testing Building The Components

The software can be downloaded by doing

		/> git clone https://github.com/ONSdigital/ras-compose.git

To build the software - which will pull all dependencies and sub components you can run the shell script
called build like:

		/> cd ras-compose
		/> ./build

This will pull down all the repos and place in docker containers with subdirectories from the branch. Your directory
tree should now look like:

		-rwxr-xr-x  1 nherriot nherriot  1738 Jan 27 14:56 build.sh
		-rwxr-xr-x  1 nherriot nherriot   424 Jan 27 14:56 cmd.sh
		drwxr-xr-x  2 nherriot nherriot  4096 Jan 27 14:56 curl
		-rw-r--r--  1 nherriot nherriot   643 Jan 27 14:56 docker-compose.yml
		-rw-r--r--  1 nherriot nherriot  1068 Jan 27 14:56 LICENSE
		drwxr-xr-x 11 nherriot nherriot  4096 Jan 27 14:57 ras-authentication
		drwxr-xr-x  4 nherriot nherriot  4096 Jan 27 14:57 ras-config
		drwxr-xr-x  3 nherriot nherriot  4096 Jan 27 14:57 ras-config-files
		drwxr-xr-x  4 nherriot nherriot  4096 Jan 27 14:57 ras-gateway
		drwxr-xr-x  4 nherriot nherriot  4096 Jan 27 14:57 ras-registry
		drwxr-xr-x  4 nherriot nherriot  4096 Jan 27 14:57 ras-respondent
		-rw-r--r--  1 nherriot nherriot 15254 Jan 27 14:56 README.md
		-rwxr-xr-x  1 nherriot nherriot   268 Jan 27 14:56 run.sh




### Testing Running The Components

At this point we are going to run only a few commands from the run.sh script. Since it contains docker commands it
makes sense to run each one individually and provide command output to help with setup. You can do a 'more' on the
run.sh command. Try this:

1) Use docker to pull down any containers that may already be running.

		/> sudo docker-compose down

2) Build any docker images that are in this directory and create the containers

		/> sudo docker-compose build

3) Bring up the images into a container in a detached mode.

		/> sudo docker-compose up -d
		[sudo] password for nherriot:
		Creating network "rascompose_ras" with the default driver
		Creating rascompose_ras-registry_1
		Creating rascompose_ras-authentication_1
		Creating rascompose_ras-respondent_1
		Creating rascompose_ras-config_1
		Creating rascompose_ras-gateway_1
		Creating rascompose_ras-frontstage_1


4) Lets just check to see what containers are up and running on docker. Using the docker ps command you should see
something like this:

		~/virtalenv/testONS/ras-compose $ sudo docker ps
		CONTAINER ID        IMAGE                           COMMAND                  CREATED              STATUS              PORTS                    NAMES
		3b9cecb8964f        rascompose_ras-gateway          "/bin/sh -c 'java ..."   About a minute ago   Up About a minute                            rascompose_ras-gateway_1
		49df20506690        rascompose_ras-frontstage       "/bin/sh -c 'pytho..."   About a minute ago   Up About a minute   0.0.0.0:5000->5000/tcp   rascompose_ras-frontstage_1
		fee2cae4d9e5        rascompose_ras-config           "/bin/sh -c 'java ..."   About a minute ago   Up About a minute                            rascompose_ras-config_1
		391d820ed21b        rascompose_ras-respondent       "/bin/sh -c 'java ..."   About a minute ago   Up About a minute                            rascompose_ras-respondent_1
		0c87d7c693d1        rascompose_ras-authentication   "/bin/sh -c './gra..."   About a minute ago   Up About a minute                            rascompose_ras-authentication_1
		b6ce35d01391        rascompose_ras-registry         "/bin/sh -c 'java ..."   About a minute ago   Up About a minute                            rascompose_ras-registry_1

You will see that the component called rascompose_ras-frontstage has an open TCP port running on local host:5000
Go to your browser and open this port on localhost i.e. http://localhost:5000/ You should see hello world! :-)



