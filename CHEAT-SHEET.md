# ras-compose Cheat Sheet
This is a short doc to consolidate many CLI commands that we as a team use to help setup, configure or diagnose issues
on the system. There are currently 2 systems in play at the moment. One is docker, and the other is cloud foundry. Both
systems provide similar functionality depending on what and how you want to achieve.

The document is split into the following parts:
1) Cloud Foundry commands
2) Docker commands
3) How to create a local Jenkins server using docker
4) Deprecated commands or systems


At the time of writing there is an Amazon instance that is hosting an implementation of cloud foundry.

## Cloudfoundry Commands

### General Information

Before you star. Cloudfoundary has a command line interface (CLI) which allows you to communicate with remote systems.
At the moment I'm using the most up-to-date tool for this which you can [get from here.](https://cli.run.pivotal.io/stable?release=linux64-binary&version=6.26.0&source=github-rel)

Place this tar file into where you keep 'applications' and create a cloud foundry folder. This will keep all 3rd party
applications in one place where you can easily manage. Untar your file and it will create a dir called:

    /cf-cli_6.26.0_linux_x86-64/

The executable to use is 'cf'. To view help commands you can do:

    />  cf  help


### Getting Started

The ONS has an instance of Cloudfoundary that is being used for development. Speak to Rob Smart to get a login. If you
have a login already then you can change your login here:

https://login.system.mvp.onsclofo.uk/login

You can also use Pivotal Web Services (PWS)to do the exact same thing. I recommend doing this so you can test with 2
systems. To setup an account go here: https://login.run.pivotal.io/




To login to the ONS system we need to use the CF tool. This uses OAuth2 to obtain a token. Once you specify the API you
want to access it obtains a token and uses this to communicate with your endpoints.

    />  cf login  -u  <user name>  -p <password>

e.g.

    />  cf login  -u  nherriot  -p  my-password

You are presented with a request for a domain to access - which is an API endpoint. We are using the API domain:
        https://api.system.mvp.onsclofo.uk

e.g.

    />  cf login  -u  nherriot  -p  my-password
    />  API endpoint: https://api.system.mvp.onsclofo.uk
    />  Authenticating...
    />  OK


To login to the PWS Cloud Foundry you need to login to the specific API endpoint. Save yourself hours of googling and
read the CLI command below - this shows me logging into my Pivotal account. For me I have used the attributes:
1) API gateway:     api.run.pivotal.io
2) User name:       Nicholas.Herriot@gmail.com
3) Your password:   xxxxxxxxx

/>  cf login -a api.run.pivotal.io -u Nicholas.Herriot@gmail.com -p xxxxxxxxxx
    API endpoint: api.run.pivotal.io
    Authenticating...
    OK

    Targeted org ONS-Test-Space

    Targeted space development

    API endpoint:   https://api.run.pivotal.io (API version: 2.84.0)
    User:           Nicholas.Herriot@gmail.com
    Org:            ONS-Test-Space
    Space:          development

Note: Do NOT use the login URL - You have to use the api URL. This will then pass a json object to your CLI command that
has the correct login URL. The CLI tool does this, but can be very misleading!



### Verify Your CF Instance Works And Looking At All Running Applications

Once you have logged in you will not know or see any prompt to indicate this. As previously mentioned the CF tool maintains
an OAuth2 token it uses to issue commands on your behalf. You can check that you can see you system applications by using
the 'app' key word. e.g.


    />  cf apps
    Getting apps in org rmras / space dev as nherriot...
    OK

    name                             requested state   instances   memory   disk   urls
    response_management_ui           started           1/1         512M     1G     response_management_ui.apps.mvp.onsclofo.uk
    iacsvc                           started           1/1         1G       1G     iacsvc.apps.mvp.onsclofo.uk
    ras-frontstage                   started           1/1         512M     1G     ras-frontstage.apps.mvp.onsclofo.uk
    rm-collection-exercise-service   stopped           0/1         512M     1G     rm-collection-exercise-service.apps.mvp.onsclofo.uk
    ras-collection-instrument-demo   started           1/1         512M     1G     ras-collection-instrument-demo.apps.mvp.onsclofo.uk
    ras-backstage-ui                 started           1/1         512M     1G     ras-backstage-ui.apps.mvp.onsclofo.uk
    casesvc                          started           1/1         1G       1G     casesvc.apps.mvp.onsclofo.uk
    ras-collection-instrument        started           1/1         512M     1G     ras-collection-instrument.apps.mvp.onsclofo.uk
    ras-party                        started           1/1         512M     1G     ras-party.apps.mvp.onsclofo.uk
    surveysvc                        stopped           0/1         256M     1G     surveysvc.apps.mvp.onsclofo.uk
    Nick_Herriot_ras_test            started           1/1         512M     1G     django-oauth2.apps.mvp.onsclofo.uk
    django-oauth2                    started           1/1         512M     1G     django-oauth2.apps.mvp.onsclofo.uk
    static-creds-broker              started           1/1         256M     1G     broker.apps.mvp.onsclofo.uk
    ras-collection-exercise-demo     started           1/1         512M     1G     ras-collection-exercise-demo.apps.mvp.onsclofo.uk


### Getting Environment Variables For An Application

You can obtain environment variables from your application using the 'env' keyword. You need to supply the command with
the application name you wish to interrogate. This is usefull to see that an application can bind to a service or 'see'
another application running on the system. Hence to see the application 'Nick_Herriot_ras_test' you can do:

        />  cf env Nick_Herriot_ras_test
        Getting env variables for app Nick_Herriot_ras_test in org rmras / space dev as nherriot...
        OK

        System-Provided:


        {
         "VCAP_APPLICATION": {
          "application_id": "c11a609b-9ecd-4675-8906-1388d9803017",
          "application_name": "Nick_Herriot_ras_test",
          "application_uris": [
           "django-oauth2.apps.mvp.onsclofo.uk"
          ],
          "application_version": "62d7282b-0e35-441b-8b34-fc780629ff09",
          "cf_api": "https://api.system.mvp.onsclofo.uk",
          "limits": {
           "disk": 1024,
           "fds": 16384,
           "mem": 512
          },
          "name": "Nick_Herriot_ras_test",
          "space_id": "b88746fd-af4a-461f-92bc-a7888de4f273",
          "space_name": "dev",
          "uris": [
           "django-oauth2.apps.mvp.onsclofo.uk"
          ],
          "users": null,
          "version": "62d7282b-0e35-441b-8b34-fc780629ff09"
         }
        }

        No user-defined env variables have been set

        No running env variables have been set

        No staging env variables have been set



### Setting and Using Environment Variables on the Fly

Often you will want to test or inject environment variables on the fly to a running system. e.g. You want to test that
your system can connect to another system like a service (DB, API, Micro Service). This takes 3 steps,
1) to view your environment variables for a running system
2) set the environment variables
3) restart your system to make those environment variables active in your running container

#### View Environment Variable

To view do:

    />  cf env <app_name>


#### Set Environment Variables

To set a variable you use the 'set-env' name. This requires your app or container name:

    />  cf  set-env  Nick_Herriot_ras_test MY_TEST this_is_a_test

You can view your change by simply running the cf env command. However you will not have access to your environment
variable unless the system restarts!



#### Making Your Environment Variable Active

You environment variable is set but how do you activate it? You can restage your application. Do this:

    />  cf restage Nick_Herriot_ras_test




## Docker Commands

After you have brought the system up with the 'docker-compose up -d' command you may find the following commands useful.

1) How do I see active docker containers and all containers/images on my machine

You can see the running and active containers with the docker command:

    /> docker ps

You can see all containers and images on your machine - this includes all that are not running at that point in time
with the command:

    /> docker ps -a


2) How do I get a shell prompt onto a container.

If the container name is 'foo-bar' then do:

/> docker exec -i -t foo-bar /bin/bash

You can also use ID number.

3) How do I find out the IP address of a docker container?

You can use the docker inspect command. This shows lots of info, near the bottom of the screen you can see the network
IP and network gateway. You need to know the name of the container. e.g. container is called foo-bar

/> docker inspect foo-bar
        "NetworkSettings": {
        ......
            "Ports": {
                "8080/tcp": [
                    {
                        "HostIp": "0.0.0.0",
                        "HostPort": "8888"
                    }
                ]
            },
        ......
                "rascompose_ras": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": [
                        "ras-authentication",
                        "612976bd17f3"
                    ],
                    "NetworkID": "7c221ffb8c54cb37a870a78bf143c084c2081321e7f138726b003ba2d3d08ea5",
                    "EndpointID": "15619538cd76f2f34dd0e07d13407779eb1cbcd072135f649ae7912e726bef80",
                    "Gateway": "172.18.0.1",
                    "IPAddress": "172.18.0.2",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "02:42:ac:12:00:02"


4) How do I find out the IP address of a docker container from within the container?

You can just ping the container or other containers from within the container. So if you were on a shell prompt from
within the container you could do:

	/> ping foo-bar

	Output would look something like:

	root@dc953f7b235c:/app# ping rascompose_ras-authentication_1
	PING rascompose_ras-authentication_1 (172.18.0.2): 56 data bytes
	64 bytes from 172.18.0.2: icmp_seq=0 ttl=64 time=0.159 ms

	root@dc953f7b235c:/app# ping rascompose_ras-gateway_1
	PING rascompose_ras-gateway_1 (172.18.0.4): 56 data bytes
	64 bytes from 172.18.0.4: icmp_seq=0 ttl=64 time=0.053 ms

5) Can I curl a container from within a container.

Yes. Once you are in a shell you can curl the internal IP address or the container name using the curl command. To show
an example of this we can curl the Flask app (ras-frontstage) on port 5000 via the ras-gateway.

	root@dc953f7b235c:/app# curl http://172.18.0.6:5000
	Hello, World from the Frontstage!

or:

	root@dc953f7b235c:/app# curl http://rascompose_ras-frontstage_1:5000
	Hello, World from the Frontstage!


6) How do I stop a specific container?

Find out the container name or ID with /> docker ps . Once you have this use the name to stop just that container. e.g.
If I want to stop the ras frontstage on my machine I would do:

    /> docker stop rascompose_ras-frontstage_1


7) Docker images are taking up all my disk space how do I fix this?

    #!/bin/bash
    #Delete all containers
    /> docker rm $(docker ps -a -q)

    #Delete all images
    /> docker rmi $(docker images -q)

   #Delete all ras images only (Use with care and understand the
   #implications of this pattern match

   />docker rmi $(docker images | grep "^ras" | awk "{print $3}")#
   Delete all ras images only (Use with care and understand the
   implications of this pattern match

   />docker rmi $(docker images | grep "^ras" | awk "{print $3}")#
   Delete all ras images only (Use with care and understand the
   implications of this pattern match

   />docker rmi $(docker images | grep "^ras" | awk "{print $3}")


## How to create a local Jenkins server using docker

If you wish to create a local jenkins server to do jobs and push to cloud foundry it's best to do this in a docker
image which will save you time in configuring and setting up. The instructions will show you how to download an image,
run it and map the directories of that image to a local folder so that the next time you start the container it will
persist data.


### Getting Jenkins for docker - mapping directory and mapping local ports.

Docker Hub already has a packaged Jenkins container. We will download this image, run it, name it 'Jenkins', map our
ports to 8082:8000 5000:5000 and mount a local folder as a volume on our container.

If we have a directory called '~/docker-jenkins/jenkins' that we wish to map as a volume our command to do this is:

    /> `docker run --name jenkins -p 8082:8080 -p 50000:50000 -v ~/docker-jenkins/jenkins:/var/jenkins_home jenkins`

### Getting your Jenkins password

The initial jenkins password will be shown on the log screen. But you can find it in the /jenkins/secrets directory.
Go to http://localhost:8082 to get your login screen

### Starting Jenkins Container

To start your container at some subsequent time use the docker start command:

    /> docker start jenkins

## Deprecated Commands or Systems

This section contains commands and instructions for systems that are at this moment no longer used.

### Config For UUA (ras-authentication)


1) Where is the main config file for UAA?

This specifies where to look or change to get certain behaviour from this component.
The main configuration file for this component is uaa.yml file. There are over 11 uaa.yml files within the ras-authenticate
folder. The one to use is in:

    /ras-authentication/ras-config/uaa.yml

2) How do I add users to my base config so that I can test a new user?

Update the users section of the yml file with users you wish to be on the system within the /ras-config/uaa.yml file.

    scim:
      users:
        - paul|wombat|paul@test.org|Paul|Smith|uaa.admin
        - stefan|wallaby|stefan@test.org|Stefan|Schmidt



3) What is the API endpoint to authenticate a user?



4) How to I check that those users exist and are working properly?




5) What do I get in a response to the UAA if the user is not on the system?









### Config For Zuul (ras-gateway)

This specifies where to look or change to get certain behaviour from this component.

1) Can I manually force a path to be routed through Zuul for testing?


2) What is the main config file to control this component?





