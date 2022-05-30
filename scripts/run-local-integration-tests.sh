tput clear
source ./scripts/common.sh
setProjectsBase

API_PROJECT_NAME=${1}
STREAM_PROJECT_NAME=${2}
CLIENT_PROJECT_NAME=${3}

validateParameters ${API_PROJECT_NAME} ${STREAM_PROJECT_NAME} ${CLIENT_PROJECT_NAME}

export $(cat .env | xargs)

# find project structure
export API_PROJECT_DIR="${PROJECTS_BASE}/${API_PROJECT_NAME}"
export STREAM_PROJECT_DIR="${PROJECTS_BASE}/${STREAM_PROJECT_NAME}"
export CLIENT_PROJECT_DIR="${PROJECTS_BASE}/${CLIENT_PROJECT_NAME}"

# setup log directory and files
export LOG_DIR="log"
export API_LOG_FILE="${LOG_DIR}/api_server.txt"
export STREAM_LOG_FILE="${LOG_DIR}/stream_server.txt"
export MOCKUSER_LOG_FILE="${LOG_DIR}/mockuser.txt"
export HOST_LOG_FILE="${LOG_DIR}/host.txt"

# setup virtual environment
export SCRATCH_DIR="${STREAM_PROJECT_NAME}/tmp"
export CLIENT_ENV_NAME="client-venv"
export STREAM_ENV_NAME="stream-server-venv"
export API_ENV_NAME="api-server-venv"
export CLIENT_ENV_DIR="${PROJECTS_BASE}/${SCRATCH_DIR}/${CLIENT_ENV_NAME}"
export STREAM_ENV_DIR="${PROJECTS_BASE}/${SCRATCH_DIR}/${STREAM_ENV_NAME}"
export API_ENV_DIR="${PROJECTS_BASE}/${SCRATCH_DIR}/${API_ENV_NAME}"

# define requirements file
export REQUIREMENTS_FILE="requirements.txt"

# setup test server addresses
export STREAM_SERVER_PORT=8001
export HULSE_STREAM_URL="http://localhost:${STREAM_SERVER_PORT}/"
export API_SERVER_PORT=8002
export HULSE_API_URL="http://localhost:${API_SERVER_PORT}/"
export TMP_FILE="${STREAM_PROJECT_DIR}/.tmp"

# optionally removing tmp file & logs
if [ -d "${LOG_DIR}" ]; then
    printf "Removing ${LOG_DIR} directory\n"
    rm -rf $LOG_DIR && mkdir $LOG_DIR
fi

if [ -f "${TMP_FILE}" ]; then
    printf "Removing ${TMP_FILE} file\n"
    rm $TMP_FILE
fi

# checking if python virtual envs are properly setup
if [ ! -d "${API_ENV_DIR}" ]; then
    tput clear
    printf "Installing API server dependencies to ${API_ENV_DIR}\n"
    python -m venv ${API_ENV_DIR}
    source ${API_ENV_DIR}/bin/activate
    echo ${API_ENV_DIR}/bin/activate
    pip install -r ${API_PROJECT_DIR}/${REQUIREMENTS_FILE}
    echo ${API_PROJECT_DIR}/${REQUIREMENTS_FILE}
    deactivate
fi

if [ ! -d "${STREAM_ENV_DIR}" ]; then
    tput clear
    printf "Installing Stream server dependencies to ${STREAM_ENV_DIR}\n"
    python -m venv ${STREAM_ENV_DIR}
    source ${STREAM_ENV_DIR}/bin/activate
    pip install -r ${STREAM_PROJECT_DIR}/${REQUIREMENTS_FILE}
    deactivate
fi

if [ ! -d "${CLIENT_ENV_DIR}" ]; then
    tput clear
    printf "Installing Client dependencies to ${CLIENT_ENV_DIR}\n"
    python -m venv ${CLIENT_ENV_DIR}
    source ${CLIENT_ENV_DIR}/bin/activate
    pip install -r ${CLIENT_PROJECT_DIR}/${REQUIREMENTS_FILE}
    cd ${CLIENT_PROJECT_DIR}
    pip install -e .
    cd ${STREAM_PROJECT_DIR}
    deactivate
fi

# run both servers in the background
tput clear
bash ${API_PROJECT_DIR}/scripts/run-server.sh &> $API_LOG_FILE &
sleep 5 # wait for the api server to start
bash ${API_PROJECT_DIR}/scripts/create-mockuser.sh &> $MOCKUSER_LOG_FILE
bash ${STREAM_PROJECT_DIR}/scripts/run-server.sh &> $STREAM_LOG_FILE &
sleep 5 # wait for the stream server to start
# run host & client tests
bash ${STREAM_PROJECT_DIR}/scripts/run-host.sh &> $HOST_LOG_FILE &
sleep 2 # wait for host to start before running client tests
bash ${STREAM_PROJECT_DIR}/scripts/run-client-tests.sh

# kill all servers & background python processes
killall python Python