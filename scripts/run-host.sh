export $(cat .env | xargs)

if [ -z $MOCK_API_KEY ]; then
    printf "Provide the mock api key required for integration test"
    exit 77
fi

if [ -z $CLIENT_ENV_DIR ]; then
    printf "Provide the path to the client virtual env"
    exit 77
fi

source "${CLIENT_ENV_DIR}/bin/activate"
hulse host --key=$MOCK_API_KEY