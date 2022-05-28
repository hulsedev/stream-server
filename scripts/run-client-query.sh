# load env variables into current env
export $(cat .env.tmp | xargs)
export $(cat .env.local | xargs)

echo $$ >> $PID_FILE

# setup development version of hulse host
source ../venv/bin/activate
cd ../hulse-py/ && pip install -e .

# TODO: add client query file call here