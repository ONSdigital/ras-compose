# ras-compose Cheat Sheet
This is a short doc to consolidate many CLI commands that we as a team use to help setup, configure or diagnose issues
on the system.

## Docker Commands

After you have brought the system up with the 'docker-compose up -d' command you may find the following commands useful.

1) How do I see active docker containers

/> docker ps

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

You can just ping the container or orther containers from within the container. So if you were on a shell prompt from
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





