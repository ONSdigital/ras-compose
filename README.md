# ras-compose
Developer environment for RAS components.


# How To Guide Getting Dev Environment Up For Ubuntu 16.04 Or Derivative (e.g. Mint 18)


## Preamble
This guide is written after trial on Linux Mint 18, hence may have text fields in example related to this.
Linux Mint 18 is a derivative of Ubuntu 16.04, all commands should work.

## Introduction
This guide should step you through the steps needed to get a default Linux distro to the point where you can
spin up docker containers on your machine. Each container will pull down the relevant source code to run the
application software for each service.
Each container will map to a Pivital [CloudFoundary Microservice](https://content.pivotal.io/microservices),
with the exception of a python web app using the python Flask micro service.

## Software Components Recommended


## Software Components Needed


## Setting Up Java



## Setting Up VirtualEnvWrapper



## Setting Up Docker

Docker is needed to run the microservice in isolated containers (there are lots of them!) We could use VM's, Vagrant and
ansible - however the environment needed to support multiple (6 minimum) servers each with a micro service is not
feasible. A Docker container is based on a chroot environment and hence does not need the machine resources to run
that a virtual machine would. More info on Docker can be [found here](https://www.docker.com/what-docker)

On your system you will need 3 docker components running on your machine each documented below

### Docker and Docker Engine
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


### Docker Machine
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

### Docker Container
The Docker Container app is used for running scripts that control (i.e. start, stop, build and create) containers.
It's an orchestration layer based on the open source 'fig' project. The version required is 1.8.1. First lets
download it directly to our /usr/local/bin directory for our particular machine architecture:

	/> sudo curl -o /usr/local/bin/docker-compose -L "https://github.com/docker/compose/releases/download/1.8.1/docker-compose-$(uname -s)-$(uname -m)"

You can use wget and a mv command if you wish, I just used this out of convenience and can't be bothered
changing the one above.




## Setting Up Gradle



## Testing Docker Works

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

	





## Testing Building The Components



## Testing Running The Components



