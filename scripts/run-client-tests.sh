export $(cat .env | xargs)

if [ -z $STREAM_PROJECT_DIR ]; then
    printf "Provide the directory of the stream project"
    exit 77
fi

if [ -z $CLIENT_ENV_DIR ]; then
    printf "Provide the path to the client virtual env"
    exit 77
fi

source "${CLIENT_ENV_DIR}/bin/activate"
#pytest ${STREAM_PROJECT_DIR}/tests/* -x --full-trace
printf "Reached here 🚀🚀🚀 ready to run some integration tests!"