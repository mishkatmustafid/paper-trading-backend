# Paper Trading Backend

Backend application service for Paper Trading website. This service provides backend functionality of the project.

## Installation

This section describes tools and configurations needed to make local environment ready for developing and running the application.

### Prerequisites

Following tech stacks are required to get the local env up and running.

- Python 3.9
- Pipenv
- Alembic
- PostgresSQL

### Installing

Once above stacks are installed and ready; execute the following commands from the root of the project

```sh
# to create and enable virtual env for the project.
$ pipenv shell

# install dependencies
$ pipenv install

# make start script executable
$ chmod +x start

# start the project
./start
```

Once service is up and running successfully hover over the following url for the API documentation:
[localhost:9000/docs](http://127.0.0.1:9000/docs)
