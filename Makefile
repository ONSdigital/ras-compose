REPOS="django-oauth2-test" "ras-collection-instrument" "ras-frontstage" "ras-party" "ras-secure-message"


NO_COLOR=\033[0m
GREEN=\033[32;01m
RED=\033[31;01m
YELLOW=\033[33;22m

all: full check-env clone build

full:
	@ printf "\n[${GREEN} Running full build. Please be patient this may take awhile! ${NO_COLOR}]\n"

check-env:
ifndef RAS_HOME
	$(error RAS_HOME environment variable is not set.)
endif
	@ printf "\n[${YELLOW} RAS_HOME set to ${RAS_HOME} ${NO_COLOR}]\n"

clone: check-env
	@ printf "\n[${YELLOW} Cloning into ${RAS_HOME} ${NO_COLOR}]\n"
	@ for r in ${REPOS}; do \
		echo "($${r})"; \
		if [ ! -e ${RAS_HOME}/$${r} ]; then \
			git clone git@github.com:ONSdigital/$${r}.git ${RAS_HOME}/$${r}; \
		else \
			echo "  - already exists: skipping"; \
		fi; echo ""; \
	done

update: check-env
	@ printf "\n[${YELLOW} Updating/Cloning repos in ${RAS_HOME} ${NO_COLOR}]\n"
	@ for r in ${REPOS}; do \
		echo "($${r})"; \
		if [ ! -e ${RAS_HOME}/$${r} ]; then \
			git clone git@github.com:ONSdigital/$${r}.git ${RAS_HOME}/$${r}; \
		else \
			cd ${RAS_HOME}/$${r}; \
			echo "On branch [`git symbolic-ref --short HEAD`], updating repo..."; \
			git pull; cd; \
		fi; echo ""; \
	done

start:
	@ printf "\n[${YELLOW} Bringing up docker compose ${NO_COLOR}]\n"
	docker-compose up

build: check-env
	@ printf "\n[${YELLOW} Refreshing build ${NO_COLOR}]\n"
	docker-compose build
