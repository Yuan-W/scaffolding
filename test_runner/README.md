# Test Runner Service

This service runs tests againsts user submitted code and returns which tests are failing.

## API

POST to `/test/` with 2 params:
- code: the code you want to test
- testCode: the test code you want run

The service will concatenate code and testCode and run it. It will parse the results of the assertions and send them as a response.

## Setup

- Run `npm install`
- install docker
- run `brew install coreutils` (OS X) or whatever toolchain which allows you to use `timeout` or `gtimeout`
- run `sh ./setup/UpdateDocker.sh`
- on Ubuntu, you need to replace `gtimeout` with `timeout` in `DockerTimeout.sh`
- `npm start` will run the server on port 3000
- `npm run dev` will run a server that restarts on code change on port 3000

## Debugging
To debug within Docker you can run:
`docker run -it -v "./temp/{someTempData}":/usercode virtual_machine bash`
