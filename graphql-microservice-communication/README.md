# Using Graphql for microservice communication

This app uses the _open source versions_ of the following tools:
- [Space Cloud](https://space-cloud.io/) as a graphql engine.

> Here's a link to the YouTube video explaining this setup in greater detail - [https://youtu.be/jUhacrwEwDk](https://youtu.be/jUhacrwEwDk)

## Prerequisites
 
- You'll need to have [Docker](https://docs.docker.com/engine/install/) installed. This project uses `docker-compose` to bring the backend components up.

## Setting up the environment

- Clone this repo and `cd` into the `graphql-microservice-communication` directory.
- Simply run `docker-compose -p graphql-demo up -d` to bring up the entire stack along with the services. 

## GraphQL as an API Aggregator
- Once all the containers are up, Open `http://localhost:4122` in a browser window.
- Configure space cloud
### Using CLI
- Install [space-cli](https://docs.docker.com/engine/install/) 
- Run the command ```space-cli apply ./config-files``` to configure space cloud
### Using UI

## GraphQL as an Data Layer
- Once all the containers are up, Open `http://localhost:4122` in a browser window.
- Configure space cloud
### Using CLI
- Install [space-cli](https://docs.docker.com/engine/install/) 
- Run the command ```space-cli apply ./config-files``` to configure space cloud
### Using UI
-