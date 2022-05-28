# Integration Tests
Provide some integration testing scripts to be run with the `scripts/run-local-integration-tests.sh` file or CI testing processes.

## Testing locally
The `scripts/run-local-integration-tests.sh` combines multiple scripts to run 4 components in parallel:
- 1 api server
- 1 stream server (both connected to the same test database)
- 1 instance of the hulse host
- 1 instance of the hulse client running queries (under a test script)

## Testing in CI
The continuous integration is hosted with Github Actions. It performs the following operations:
- fetch the api and stream server source code from github repos
- fetch the 
