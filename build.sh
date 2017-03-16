#!/bin/bash


REPOS="django-ouath2-server ras-collection-instrument ras-frontstage ras-collection-instrument ras-respondent ras-gateway ras-registry ras-authentication" # Not currently used: ras-config ras-config-files
PARENT=`pwd`


# Rebuild .gitignore
echo ".gitignore" > .gitignore


function clone {

  # Get the repo name and URL:
  name=$1
  repo=$2
  PARENT=`pwd`

  # Make sure we have a non-blank directory name, just in case:
  if [ ! -z "$name" ]
  then

    # Get code

    if [ ! -d "$name" ]
    then
      echo - cloning $repo
      git clone $repo
    else
      echo - Updating $repo
      cd $name
      git pull --rebase
    fi

    # Build up .gitignore

    cd $PARENT
    echo $name >> .gitignore
    #debug: cat .gitignore

  else
    Error: please provide a repository name and a repo URL. $name $repo
    exit 1
  fi

  cd $PARENT
}


# Bulid Java projects

for name in $REPOS
do
  # Make sure we have a non-blank repo name, just in case:
  if [ ! -z "$name" ]
  then

    # Get code

    repo="git@github.com:onsdigital/"${name}".git"
    clone $name $repo

    # Build code

    cd $name
    # NB Configuration information doesn't need a build
    if [ -f "pom.xml" ]
    then
      echo - Maven building $name
      mvn clean package
    elif [ -f "build.gradle" ]
    then
      # Build anything but Cloudfoundry. That needs to be built on container build because it's "special".
      if [ "$name" != "ras-authentication" ]
      then
        echo - Gradle building $name
        # Build using the host machine..
        #gradle clean build
        # ...or use a temporary container to run the build:
        docker run -it --rm --volume `pwd`:/root --volume $HOME/.gradle:/root/.gradle frekele/gradle gradle clean build
      fi
    fi
    cd $PARENT

    # Build .gitignore

    echo $name >> .gitignore

  fi
done
