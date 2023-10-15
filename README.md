# Crate Optimizer FastAPI API

This FastAPI API provides a single endpoint for optimizing the number of crates required for a specific order.

## Getting Started

To get the application up and running, follow these steps:

### Prerequisites

- Docker.
- docker-compose.

### Build the Docker Image

Run the following command to build the Docker image:
```shell
docker-compose build
```
Run the following command to start the application:
```shell
docker-compose up
```
Run the following command to run the unit tests:

```shell
docker-compose crate-optimizer exec pytest
```

now navigate to http://localhost:8000/docs and start playing arround.
