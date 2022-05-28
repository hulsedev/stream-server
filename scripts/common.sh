# common functions taken from https://github.com/hasii2011/CodeSigningScripts

fgBlack=$(tput setaf 0) 	# black
fgRed=$(tput setaf 1) 		# red
fgGreen=$(tput setaf 2) 	# green
fgYellow=$(tput setaf 3) 	# yellow
fgBlue=$(tput setaf 4) 		# blue
fgMagenta=$(tput setaf 5) 	# magenta
fgCyan=$(tput setaf 6) 		# cyan
fgWhite=$(tput setaf 7) 	# white
#
txBold=$(tput bold)   		# bold
txHalf=$(tput dim)    		# half-bright
txUnderline=$(tput smul)   	# underline
txEndUnder=$(tput rmul)   	# exit underline
txReverse=$(tput rev)    	# reverse
txStandout=$(tput smso)   	# standout
txEndStand=$(tput rmso)   	# exit standout
txReset=$(tput sgr0)   	    # reset attributes

function printError() {
    errorMsg=$*
    printf "${txBold}${fgRed}$*${txReset}\n"
}

function setProjectsBase() {
    if [[ -z "${PROJECTS_BASE}" ]]; then
        export PROJECTS_BASE="/Users/sachalevy/implement"
    fi
    printf "Projects base directory: ${txReverse}${PROJECTS_BASE}${txReset}\n"
}

function setAPIProjectName() {
    if [[ -z "${API_PROJECT_NAME}" ]]; then
        export API_PROJECT_NAME="django-feed-auth0"
    fi
    printf "API project root directory: ${txReverse}${API_PROJECT_NAME}${txReset}\n"
}

function setStreamProjectName() {
    if [[ -z "${STREAM_PROJECT_NAME}" ]]; then
        export STREAM_PROJECT_NAME="hulse-stream"
    fi
    printf "Stream project directory name: ${txReverse}${STREAM_PROJECT_NAME}${txReset}\n"
}


function doParamsExist() {
    API_PROJECT_NAME=${1}
    STREAM_PROJECT_NAME=${2}
    CLIENT_PROJECT_NAME=${3}

    if [ -z $API_PROJECT_NAME ]; then
            printError "Provide the directory name of the api project"
            exit 77
    fi
    
    if [ -z $STREAM_PROJECT_NAME ]; then
            printError "Provide the directory name of the stream project"
            exit 77
    fi

    if [ -z $CLIENT_PROJECT_NAME ]; then
            printError "Provide the directory name of the client project"
            exit 77
    fi
}

function validateParameters() {
    API_PROJECT_NAME=${1}
    STREAM_PROJECT_NAME=${2}
    CLIENT_PROJECT_NAME=${3}

    doParamsExist ${API_PROJECT_NAME} ${STREAM_PROJECT_NAME} ${CLIENT_PROJECT_NAME}

    # do project directories exist?
    API_PROJECT_DIR="${PROJECTS_BASE}/${API_PROJECT_NAME}"
    STREAM_PROJECT_DIR="${PROJECTS_BASE}/${STREAM_PROJECT_NAME}"
    CLIENT_PROJECT_DIR="${PROJECTS_BASE}/${CLIENT_PROJECT_NAME}"

    if [ ! -d "${API_PROJECT_DIR}" ]; then
        printError "${API_PROJECT_DIR} api project directory does not exist"
        exit 88
    fi
    
    if [ ! -d "${STREAM_PROJECT_DIR}" ]; then
        printError "${STREAM_PROJECT_DIR} stream project directory does not exist"
        exit 99
    fi

    if [ ! -d "${CLIENT_PROJECT_DIR}" ]; then
        printError "${CLIENT_PROJECT_DIR} client project directory does not exist"
        exit 99
    fi
}