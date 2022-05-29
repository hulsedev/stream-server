export $(cat .env | xargs)

if [ -z $MOCK_API_KEY ]; then
    printf "Provide the mock api key required for integration test"
    exit 77
fi

if [ -z $CLIENT_ENV_DIR ]; then
    printf "Provide the path to the client virtual env"
    exit 77
fi

export MOCK_CLUSTER_NAME="mockcluster"
export MOCK_CLUSTER_DESCRIPTION="mockcluster description"

source "${CLIENT_ENV_DIR}/bin/activate"
hulse create-cluster --name="${MOCK_CLUSTER_NAME}" --description="${MOCK_CLUSTER_DESCRIPTION}" --key=$MOCK_API_KEY
hulse host --key=$MOCK_API_KEY