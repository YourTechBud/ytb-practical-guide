# Using Graphql for microservice communication

This app uses the _open source versions_ of the following tools:
- [Space Cloud](https://space-cloud.io/) as a graphql engine.

## Prerequisites
 
- You'll need to have [Docker](https://docs.docker.com/engine/install/) installed. This project uses `docker-compose` to bring the backend components up.

## Setting up the environment

- Clone this repo and `cd` into the `graphql-microservice-communication` directory.
- Simply run `docker-compose -p graphql-demo up -d` to bring up the entire stack along with the services. 

## Configuring space cloud
### Using CLI
- Install [space-cli](https://docs.docker.com/engine/install/)
- Run the command ```space-cli apply ./config-files``` in the current directory to configure space cloud
- If the above command promts you with this question ``` ? Changing the schema can cause data loss (this option will be applied to all resources of type db-schema). ```. Say ```Yes```
### Using UI
- For UI, refer the youtube video


## Scenario 1: GraphQL as an API Aggregator
- Use the below query, to get all the posts from post-service
```
query {
	getAllPosts @posts
}
```
- Use the below query, to get a single user from user-service
```
query {
    getUserById(userId: "1") @users
}
```
- Use the below query, to join data of posts with user service
```
query {
	getAllPosts @posts {
    id
    title
    getUserById(userId: "getAllPosts.userId") @users
  }
}
```

## Scenario 2: GraphQL as an Data Layer
- Use the below query, to get all the post stats from the table `post_stats`
```
query {
  post_stats(where: {post_id: "1"}) @postgres {
    post_id
    comments
    likes
    views
  }
}
```
- Use the below query, to join data of post service with database
```
query {
	getAllPosts @posts {
    id
    title
    post_stats(where: {post_id: "getAllPosts.id"}) @postgres
  }
}
```
- Finally to stick it all together, we can write a single query to get all the posts along with its stat and the user
```
query {
	getAllPosts @posts {
    id
    title
    getUserById(userId: "getAllPosts.userId") @users
    post_stats(where: {post_id: "getAllPosts.id"}, op: one) @postgres
  }
}
```