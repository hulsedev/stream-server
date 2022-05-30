# Hulse Stream Server
Server connecting clients (consumers) and hosts (producers) allowing them to seamlessly run queries.

## Getting Started

Clone the application:

```bash
git clone git@github.com:hulsedev/stream-server.git
cd stream-server
```

Next, create a virtual env & install dependencies:
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Running locally

You can directly run the app using the following script:
```bash
bash scripts/run-debug-server.sh
```

For more info on running things locally, check out the local integration test example showcased in the `tests/README.md` file.

## Deployment
The app is currently deployed on Heroku using free dynos (free credits). You can find the Heroku deployment instructions in the `Procfile`.
