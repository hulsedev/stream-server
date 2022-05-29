# Integration Tests
Provide some integration testing scripts to be run with the `scripts/run-local-integration-tests.sh` file or CI testing processes.

## Testing locally
The `scripts/run-local-integration-tests.sh` combines multiple scripts to run 4 components in parallel:
- 1 api server
- 1 stream server (both connected to the same test database)
- 1 instance of the hulse host
- 1 instance of the hulse client running queries (under a test script)

In order to run the integration test, you'll need the root directory where your api server, stream server, and hulse client projects are located, as well as the directory names of each of the projects. Run the following command, being located in the root of your stream server directory:
```bash
PROJECTS_BASE=<your-root-dir> bash scripts/run-local-integration-tests.sh <api-server-name> <stream-server-name> <client-project-name>
```
> For example, on my local machine, here is the command I am running:
> ```bash
>  PROJECTS_BASE="/Users/sachalevy/implement" bash scripts/run-local-integration-tests.sh django-feed-auth0 hulse-stream hulse-py
> ```

## Testing in CI
The continuous integration is hosted with Github Actions. We spin up 4 docker containers, and run our tests by interacting with them. For this step, we simulate our production setting by deploying 1 postgresql database, to which connect the 2 server containers (1 for api and 1 for stream), and 1 container corresponding to a mock host.