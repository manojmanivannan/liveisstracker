.DEFAULT_GOAL := help
TOPDIR=.

MAVEN_COMPOSE_ARGS:= \
		-Denv.GITLAB_REPO_URL=registry.gitlab.com/manojm18 \
		-Pgitlab-resource

OKGREEN := \033[32m
WARNING := \033[33m
FAIL    := \033[31m
ENDC    := \033[0m
BOLDYELLOW := \033[1m\033[33m
BOLDCYAN := \033[1m\033[36m
CYAN := \033[36m

clean:
	@printf "[$(OKGREEN)INFO$(ENDC)] Cleaning\n"
	@mvn clean

dk_compose_tests:
	@printf "[$(OKGREEN)INFO$(ENDC)] Running Tests\n"
	@make clean launch && (make stop; printf "[$(OKGREEN)INFO$(ENDC)] Tests passed\n") || (printf "[$(FAIL)ERROR$(ENDC)] Test failed $$? \n"; exit 1)

remove_container := false
ifdef SKIP_REMOVE_CONTAINER
override remove_container=$(SKIP_REMOVE_CONTAINER)
endif

branch_snapshot_name := $(shell .m2/gitlab_build.sh --get_version)
ifdef BRANCH_SNAPSHOT
override branch_snapshot_name=$(BRANCH_SNAPSHOT)
endif

test_user_name=
ifdef TEST_USER
override test_user_name=-u$(TEST_USER)
endif

REPO_URL := registry.gitlab.com/manojm18
REGISTRY_URL := manojmanivannan18/python-hellomaven

#py_project_version := $(shell mvn -q help:evaluate -Dexpression=project.version -DforceStdout)
#develop_image_id := $(shell docker images | grep 'registry.gitlab.com/manojmanivannan/liveisstracker' | grep develop-SNAPSHOT | tr -s ' ' | cut -d ' ' -f3)

prepare_py_container:
	@printf "[$(OKGREEN)INFO$(ENDC)] Pulling Python app base docker image\n"
	@docker pull "${REGISTRY_URL}":python-st-190; EXIT_CODE=$$?; \
	if [ "$$EXIT_CODE" -eq 0 ]; then \
		printf "[$(OKGREEN)INFO$(ENDC)] Starting up python container\n"; \
		docker run -it -d -p 8501:8501 -v "$(shell pwd)/target/generated-sources/liveisstracker/liveisstracker:/home/manoj/liveisstracker" -v "$(shell pwd)/map_secret.txt:/run/secrets/mapbox_token" -e MAPBOX_TOKEN='/run/secrets/mapbox_token' --name python_app "$(REGISTRY_URL)":"python-st-190" bash ; \
		echo copying && docker cp  "$(shell pwd)/target/generated-sources/liveisstracker/liveisstracker" python_app:/home/manoj/ \
		|| printf "[$(FAIL)ERROR$(ENDC)] Unable to run/start the python container\n" || exit 1;\
	else \
		printf "[$(FAIL)FAIL$(ENDC)] Unable to pull docker image for Python app base\n"; \
		exit 1 ;\
	fi;

run_python_tests:
	@[ "${branch_snapshot_name}" ] || \
		( printf "[$(FAIL)ERROR$(ENDC)] BRANCH_SNAPSHOT not specficied. If you are running locally pass args: BRANCH_SNAPSHOT=(.m2/gitlab_build --get_version)\n" ; exit 1 )
	@echo "-----------------------------------------------------------------------------"
	@echo "     Running python tests for $(branch_snapshot_name)"
	@echo "-----------------------------------------------------------------------------"
	@printf "[$(OKGREEN)INFO$(ENDC)] Testing python code: Developer mode : Unittest\n"
	@if [ ! -d "$(TOPDIR)/target" ]; then \
		$(MAKE) generate; \
		fi
ifneq ($(shell docker ps -q --filter="name=python_app"),)
	@printf "[$(OKGREEN)INFO$(ENDC)] Python container already running\n"
else
	@printf "[$(OKGREEN)INFO$(ENDC)] There is no python container on which the python tests can run\n"
	@make prepare_py_container
endif
	@printf "[$(OKGREEN)INFO$(ENDC)] Running test as user: $(TEST_USER)\n"
	@docker exec -t $(test_user_name) python_app bash -c "export PYTEST_ADDOPTS="-v"; python -m pytest -p no:cacheprovider tests"; EXIT_CODE=$$?; \
		if [ "$$EXIT_CODE" -ne 0 ]; then \
		printf "[$(FAIL)ERROR$(ENDC)] Python test failed !\n"; \
			if [ "$(remove_container)" = "false" ]; then \
			printf "[$(OKGREEN)INFO$(ENDC)] Removing python containers on which test was run\n"; \
			docker stop python_app && docker rm python_app || printf "[$(OKGREEN)INFO$(ENDC)] No containers to remove\n"; printf "exit" && exit 1 ; \
			fi ; exit 1; \
		fi
ifneq ($(remove_container),true)
	@printf "[$(OKGREEN)INFO$(ENDC)] Removing python containers on which test was run\n"
	@docker stop python_app && docker rm python_app || printf "[$(OKGREEN)INFO$(ENDC)] No containers to remove\n"
endif

run_streamlit:
	@echo "--------------------------------------------------------------------------"
	@echo "       Running Streamlit on $(branch_snapshot_name)"
	@echo "-------------------------------------------------------------------------"
	@printf "[$(OKGREEN)INFO$(ENDC)] Testing python code: Developer mode : Streamlit\n"
	@if [ ! -d "$(TOPDIR)/target" ]; then \
		$(MAKE) generate; \
		fi
ifneq ($(shell docker ps -q --filter="name=python_app"),)
	@printf "[$(OKGREEN)INFO$(ENDC)] Python container already exists\n"
	@docker stop python_app && docker start python_app
else
	@printf "[$(OKGREEN)INFO$(ENDC)] There is no python container on which the streamlit can run\n"
	@make prepare_py_container
endif
	@docker exec -t python_app bash -c "streamlit run track_iss.py"


stop:
	@printf "[$(OKGREEN)INFO$(ENDC)] Removing any and all containers related to this project\n"
ifneq ($(shell docker ps -q --filter="name=python_app"),)
	@printf "[$(OKGREEN)INFO$(ENDC)] Removing python test container\n"
	@docker stop python_app && docker rm python_app || printf "[$(OKGREEN)INFO$(ENDC)] No running Python container for test\n"
endif
	@printf "[$(OKGREEN)INFO$(ENDC)] Removing docker-compose containers\n"
	@if [ -d "$(TOPDIR)/target" ]; then \
		printf "[$(OKGREEN)INFO$(ENDC)] Stopping docker-compose\n"; \
		docker-compose down; \
		else \
		printf "[$(OKGREEN)INFO$(ENDC)] Getting resource to stop\n"; \
		make generate; \
		docker-compose down; \
		make clean; \
	fi



package:
	@echo "---------------------------------------------"
	@echo "                Packaging                    "
	@echo "---------------------------------------------"
	@printf "[$(OKGREEN)INFO$(ENDC)] Packaging\n"
	@/bin/bash .m2/gitlab_build.sh --branch $(shell git rev-parse --abbrev-ref HEAD) --git_repo_url $(REPO_URL)

#mvn -s .m2/settings.xml $(MAVEN_COMPOSE_ARGS) package

deep_clean:
	@printf "[$(OKGREEN)INFO$(ENDC)] Deep clean\n"
	@$(MAKE) clean
	@$(MAKE) stop
	@printf "[$(OKGREEN)INFO$(ENDC)] Removing unused docker volumes\n"
	@docker volume prune -f
ifneq ($(shell docker images --filter "dangling=true" -q --no-trunc),)
	@printf "[$(OKGREEN)INFO$(ENDC)] Removing unnecessary images\n"
	@docker rmi --force $(shell docker images --filter "dangling=true" -q --no-trunc)
endif
ifneq ($(shell docker images | grep 'liveisstracker'),)
	@printf "[$(OKGREEN)INFO$(ENDC)] Removing all docker images named liveisstracker\n"
	@docker rmi --force $(shell docker images | grep 'liveisstracker'  | tr -s ' ' | cut -d ' ' -f3 | uniq -c | tr -s ' ' | cut -d ' ' -f3)
endif
ifneq ($(shell docker images | grep 'python-hellomaven'),)
	@printf "[$(OKGREEN)INFO$(ENDC)] Removing all docker images named python-hellomaven\n"
	@docker rmi --force $(shell docker images | grep 'python-hellomaven'  | tr -s ' ' | cut -d ' ' -f3 | uniq -c | tr -s ' ' | cut -d ' ' -f3)
endif

generate:
	@printf "[$(OKGREEN)INFO$(ENDC)] Getting resources\n"
	@mvn -s .m2/settings.xml resources:resources #$(MAVEN_COMPOSE_ARGS)
	@printf "[$(OKGREEN)INFO$(ENDC)] Generate python project tar ball\n"
	@mvn -s .m2/settings.xml exec:exec@generate-package #$(MAVEN_COMPOSE_ARGS)

launch:
	@printf "[$(OKGREEN)INFO$(ENDC)] Bringing up containers - docker-compose\n"
	@if [ ! -d "$(TOPDIR)/target" ]; then \
		make generate; \
	fi
	@docker stop python_app || printf "[$(OKGREEN)INFO$(ENDC)] No containers to stop\n"
	@docker pull "$(REPO_URL)/liveisstracker:$(branch_snapshot_name)"; EXIT_CODE=$$?; \
		if [ "$$EXIT_CODE" -ne 0 ]; then \
		printf "[$(WARNING)WARN$(ENDC)] No registry image for current branch. Build image first !\n"; \
		printf "[$(OKGREEN)INFO$(ENDC)] Using local image if present.\n"; \
		fi;
	@$$(sed -i 's#image: registry.gitlab.*#image: $(REPO_URL)/liveisstracker:$(branch_snapshot_name)#g' docker-compose.yml)
	@docker-compose --compatibility up -d 
	@$$(sed -i 's#image: registry.*#image: registry.gitlab#g' docker-compose.yml)


help:
	@printf "$(BOLDYELLOW)Main targets:$(ENDC) $(BOLDCYAN)Live ISS Tracker$(ENDC)\n"
	@printf "$(OKGREEN)clean     		$(ENDC): Clean mvn target folder\n"
	@printf "$(OKGREEN)stop      		$(ENDC): Stop all containers and bring down docker-compose if up\n"
	@printf "$(OKGREEN)dk_compose_tests	$(ENDC): Launch the application successfully in docker-compose mode\n"
	@printf "$(OKGREEN)run_python_tests	$(ENDC): Run python package test. SKIP_REMOVE_CONTAINER=true to skip removing the docker container if tests pass.\n"
	@printf "$(OKGREEN)run_streamlit		$(ENDC): Runs the Streamlit server on the container.\n"
	@printf "$(OKGREEN)package   		$(ENDC): Builds docker images and pushes to GITLAB registry\n"
	@printf "$(OKGREEN)deep_clean		$(ENDC): Cleans mvn target folder, removes docker volumes, containers and images matching 'liveisstracker' & 'python-hellomaven'\n"
	@printf "$(OKGREEN)launch    		$(ENDC): Generates resources and brings the docker-compose up 'builds images'\n"
	@printf "$(OKGREEN)help      		$(ENDC): show this help\n"

