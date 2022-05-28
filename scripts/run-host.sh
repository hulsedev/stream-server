# load env variables into current env
export $(cat .env.tmp | xargs)
export $(cat .env.local | xargs)

# add current pid to the list of running process
echo $$ >> $PID_FILE

# setup development version of hulse host
source ../venv/bin/activate
cd ../hulse-py/ && pip install -e .
hulse host --key=$MOCK_API_KEY
