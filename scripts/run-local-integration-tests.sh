export $(cat .env.local | xargs)

LOG_DIR="log"
API_LOG_FILE="${LOG_DIR}/api_server.txt" 
STREAM_LOG_FILE="${LOG_DIR}/stream_server.txt"
MOCKUSER_LOG_FILE="${LOG_DIR}/mockuser.txt"

# run both servers in the background
source ../api-venv/bin/activate
bash ${DB_DIR}/scripts/run-server.sh &> $API_LOG_FILE &
sleep 5
bash ${DB_DIR}/scripts/create-mockuser.sh #&> $MOCKUSER_LOG_FILE

# run stream server in the background
#bash scripts/run-server.sh &
#
## re-install local development version of hulse server
#bash scripts/run-host.sh &
## run mock client queries in the background
#bash scripts/run-client-query.sh
#
## make sure remove test database
rm $DB_DIR/$DB_NAME
#rm $DB_DIR/$DB_NAME $API_LOG_FILE $STREAM_LOG_FILE $MOCKUSER_LOG_FILE
#killall python