#!/bin/bash

MVN_SETTINGS="-s .m2/settings.xml -Pgitlab-resource"
IS_TAG_BUILD=false
RET_CODE=0
GET_VERSION_ONLY=0

function do_header
{
  printf "%0$(tput cols)d" 0|tr '0' '='
  echo ""
  echo "$*"
  printf "%0$(tput cols)d" 0|tr '0' '='
  echo ""
  echo -e "\e[39m"
}

function header_green
{
  echo -e "\e[32m"
  do_header $*
}

function header_red
{
  echo -e "\e[31m"
  do_header $*
}

function header
{
  if [ "${RET_CODE}" -eq 0 ]
  then
    header_green $*
  else
    header_red $*
  fi
}

function run_mvn
{
  if [ "${RET_CODE}" -eq 0 ]
  then
    echo ""
    header "Start: mvn $*"
    mvn ${MVN_SETTINGS} $*
    RET_CODE=$?
    header "End: mvn $*"
  fi
}

function increment_version()
{
    local v=$1
    if [ -z $2 ]; then
        local rgx='^((?:[0-9]+\.)*)([0-9]+)($)'
    else
        local rgx='^((?:[0-9]+\.){'$(($2-1))'})([0-9]+)(\.|$)'
        for (( p=`grep -o "\."<<<".$v"|wc -l`; p<$2; p++)); do
            v+=.0;
        done;
    fi
    val=`echo -e "$v" | perl -pe 's/^.*'$rgx'.*$/$2/'`
    echo "$v" | perl -pe s/$rgx.*$'/${1}'`printf %0${#val}s $(($val+1))`/
}

while [ "$#" -gt 0 ]; do
  case $1 in
    --taggedBuild)
      shift
      IS_TAG_BUILD=$1
      ;;
    --branch)
      shift
      GIT_BRANCH=$1
      ;;
  --git_repo_url)
      shift
      GIT_REPO_URL=$1
      ;;
  --get_version)
      shift
      GET_VERSION_ONLY=1
      ;;
    *)
      echo "Unknown parameter: $1"
      exit 1
      ;;
  esac

  shift
done


if [ -z ${GIT_BRANCH} ]
then
  GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
fi
GIT_SANITIZED_BRANCH=$(echo ${GIT_BRANCH} | sed 's/[^ 0-9,a-z,A-Z]/-/g')
GIT_DESCRIBE=$(git describe --tags --long) # e.g. "2.0.1-1145-g5aee72ec"
GIT_DESCRIBE_VER=$(cut -d- -f1 <<< ${GIT_DESCRIBE}) # e.g. "2.0.1"
GIT_DESCRIBE_SINCE=$(cut -d- -f2 <<< ${GIT_DESCRIBE}) # e.g. "1145"
GIT_DESCRIBE_SHA=$(cut -d- -f3 <<< ${GIT_DESCRIBE}) # e.g. "g5aee72ec"
VER_MAJOR=$(cut -d. -f1 <<< ${GIT_DESCRIBE_VER})
VER_MINOR=$(cut -d. -f2 <<< ${GIT_DESCRIBE_VER})
VER_PATCH=$(cut -d. -f3 <<< ${GIT_DESCRIBE_VER})

GIT_BRANCH_TYPE="feature"
if [ "${IS_TAG_BUILD}" == "true" ] || grep -q -i master <<< "${GIT_BRANCH}"
then
  GIT_BRANCH_TYPE="release"
elif grep -q -i bugfix <<< "${GIT_BRANCH}"
then
  GIT_BRANCH_TYPE="bugfix"
elif grep -q -i develop <<< "${GIT_BRANCH}"
then
  GIT_BRANCH_TYPE="integration"
elif grep -q -i master <<< "${GIT_BRANCH}"
then
  GIT_BRANCH_TYPE="release"
fi

if [ "${IS_TAG_BUILD}" == "true" ]
then
  VER_FULL="${VER_MAJOR}.${VER_MINOR}.${VER_PATCH}"
else
    if [ "${GIT_BRANCH_TYPE}" == "integration" ]
    then
        # SNAPSHOT builds use NEXT patch number by default - Develop
        VER_FULL="${GIT_SANITIZED_BRANCH}-SNAPSHOT"
    else
        # SNAPSHOT builds use NEXT patch number by default - feature/bugfix
        let VER_PATCH=${VER_PATCH}+1
        VER_FULL="${VER_MAJOR}.${VER_MINOR}.${VER_PATCH}-${GIT_SANITIZED_BRANCH}-SNAPSHOT"
    fi
fi

MVN_SETTINGS="${MVN_SETTINGS} -Denv.newVersion=${VER_FULL}"

if [ ! -z ${GIT_REPO_URL} ]
then
    MVN_SETTINGS="${MVN_SETTINGS} -Denv.GITLAB_REPO_URL=$GIT_REPO_URL"
fi

if [ "${GET_VERSION_ONLY}" -eq 1 ]
then
    echo "${VER_FULL}";
    exit 0
fi

header "Branch info"
echo "  Branch name:      ${GIT_BRANCH}"
echo "  Branch type:      ${GIT_BRANCH_TYPE}"
echo "  Tag version:      ${GIT_DESCRIBE_VER}"
echo "  Builds since tag: ${GIT_DESCRIBE_SINCE}"
echo "  Last checkin SHA: ${GIT_DESCRIBE_SHA}"
echo ""
header "Build info"
echo "  Is tagged build?: ${IS_TAG_BUILD}"
echo "  Maven settings:   ${MVN_SETTINGS}"
echo "  Build version:    ${VER_FULL}"
echo "  Repo URL:         ${GIT_REPO_URL}"
run_mvn package

if [ "${RET_CODE}" -eq 0 ]
then
  header "Success! This build version is: ${VER_FULL}"
fi

exit ${RET_CODE}

