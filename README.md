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

### Configuration and Running

- Rename `env.sample` --> `.env`
- Fill out the env variables in the file from a team member.

Once above stacks are installed and ready; execute the following commands from the root of the project.

Start the postgres app and create a database called `papertrade_db` from the UI. Execute following commands from the root of the project.

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

### Alembic and migrations

Alembic can view the status of the database and compare against the table metadata in the application, generating the `obvious` migrations based on a comparison.

If new models are added alembic would be able to detect it. Run the following commands to create new migration version using `--autogenerate` option.

```sh
# Tpo autogenerate new version
$ alembic --config migrations/alembic.ini revision --autogenerate -m "<commit_message>"

# upgrade to the latest version
$ alembic --config migrations/alembic.ini upgrade head

```
