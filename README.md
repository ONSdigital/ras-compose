# ras-compose
Developer environment for RAS components.


# How To Guide Getting Dev Environment Up For Ubuntu 16.04 Or Derivative (e.g. Mint 18)


## Preamble
This guide is written after trial on Linux Mint 18, hence my have text fields in example related to this.
Linux Mint 18 is a derivative of Ubuntu 16.04, all commands should work.

## Introduction


## Software Components Recommended


## Software Components Needed


## Setting Up Java



## Setting Up VirtualEnvWrapper



## Setting Up Docker

Docker is needed to run the microservice in isolated containers (there are lots of them!) We could use Vagrant and
ansible - however the environment needed to support multiple (6 minimum) servers each with a micro service is not
feasible. A Docker container is based on a chroot environment and hence does not need the machine resources to run
that a virtual machine would. More info on Docker can be found here:

https://www.docker.com/what-docker

On your system you will need 3 components running on your machine each documented below

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

5) Now use the package from this repo and not your defaut. To ensure this is the case you can do:

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

2) Download a version of docker machine that is needed for your particular architecture. The move it to your
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



## Testing Building The Components



## Testing Running The Components



