# DE_Challenge

The repository for analysis of the drug and its effect

The repository is used to provide the detailed description for the problem statement requested
and also to provide the detailed description for the write up and possible techical solution.


## Quickstart

To get up and running, all you'll need to do is run `bin/setup`.

This will create a Docker-based development environment and start your service.

The Docker environment will pick up changes to your code as you make them.

Your service will be available on:

  * http://localhost:24060/v1/ui/

You can access your PostgreSQL database via pgweb at:

  * http://localhost:24061/

This repository comes with an `.editorconfig`. Make sure your editor can take
advantage of it by [installing appropriate plugins](https://editorconfig.org/#download) if needed.

## Useful Commands

The following commands may come in handy as you develop.

### `bin/aws COMMAND`

The `bin/aws` command will let you run an AWS command against LocalStack (the container that emulates AWS services).

#### Examples

* Create a Kinesis stream: `bin/aws kinesis create-stream --stream-name my-stream --shard-count 1`
* List available Kinesis streams: `bin/aws kinesis list-streams`

### `bin/exec COMMAND`

The `bin/exec` command will let you run a process inside of the running service container.

#### Examples

* Get an interactive shell: `bin/exec sh`
* Run a flask command: `bin/exec flask urls`

This is equivalent to `docker-compose exec COMMAND`

### `bin/logs`

The `bin/logs` command will display logs from your running containers.

#### Examples

* Get logs for all containers: `bin/logs`
* Follow logs for all containers: `bin/logs -f`
* Follow logs for the service container: `bin/logs -f de-challenge`

This is equivalent to `docker-compose logs`

### `bin/nuke`

The `bin/nuke` command will destroy the Docker environment entirely. Useful for troubleshooting environment issues.

This is equivalent to `docker-compose down --rmi all --volumes --remove-orphans`

### `bin/pytest`

The `bin/pytest` command will run the test suite.

### `bin/reload`

The `bin/reload` command will restart the service container.

This is equivalent to `docker-compose restart de-challenge`

### `bin/restart`

The `bin/restart` command will restart all containers (or any containers you specify).

#### Examples

* Restart all containers: `bin/restart`
* Restart postgres: `bin/restart postgres`

This is equivalent to `docker-compose restart [container1 [container2]]`

### `bin/setup`

The `bin/setup` command will rebuild the Docker environment and bootstrap the application for development.

### `bin/start`

The `bin/start` command will start all containers (or any containers you specify).

#### Examples

* Start all containers: `bin/start`
* Start postgres: `bin/start postgres`

This is equivalent to `docker-compose start [container1 [container2]]`

### `bin/stop`

The `bin/stop` command will stop all containers (or any containers you specify).

#### Examples

* Stop all containers: `bin/stop`
* Stop postgres: `bin/stop postgres`

This is equivalent to `docker-compose stop [container1 [container2]]`


## Deployment

The project contains a Dockerfile that should produce a production-ready container to host the application.
