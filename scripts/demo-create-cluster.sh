export STREAM_SERVER_PORT=8001
export HULSE_STREAM_URL="http://127.0.0.1:${STREAM_SERVER_PORT}/"
export API_SERVER_PORT=8002
export HULSE_API_URL="http://127.0.0.1:${API_SERVER_PORT}/"
hulse get-clusters --key="7bc3581294a2ad734f5814fb7d1292cbe3a6edb7"
hulse create-cluster --name="mockcluster" --description="a cool cluster" --key="7bc3581294a2ad734f5814fb7d1292cbe3a6edb7"