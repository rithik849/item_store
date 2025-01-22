# Item Store App

## Tech stack

* ### Frontend

  * React
* ### Backend

  * Django
  * Django Rest Framework
* ### Database

  * PostgreSQL


## How to run

### Note: All commands are run from the main repo directory

### Create an empty directory called data in the db_volume directory:

`mkdir db_volume/data`

Make sure db_volume is part of the Docker File Sharing directory list.

Open the Docker Desktop App and go to:

Settings -> Resources -> File Sharing

Ensure the path to db_volume is included in the Virtual File Share list.

### Run the following commands:

`docker compose build`

`docker compose up`

To access the frontend, open the browser at localhost:3000.

To access the backend Browsable API open the browser at localhost:8000.
