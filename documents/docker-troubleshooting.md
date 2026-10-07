# Docker Troubleshooting Guide

## Container Exited

A Docker container may exit when the main process inside the container stops.

Useful commands:

docker ps
docker ps -a
docker logs <container-name>
docker inspect <container-name>

## Container Restarting

A container that repeatedly restarts may have:

- Application startup failure
- Missing environment variables
- Incorrect configuration
- Dependency connection failure

Useful commands:

docker ps
docker logs <container-name>
docker inspect <container-name>

## Image Problems

If an image cannot be started, check:

- Image name
- Image tag
- Image architecture
- Environment variables
- Application configuration

Useful commands:

docker images
docker pull <image>
docker inspect <image>
