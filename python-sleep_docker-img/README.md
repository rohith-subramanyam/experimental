# python-sleep docker image
This is a docker image with a python process that prints the current time, sleeps for 2 seconds and repeats until it is interrupted.
## How to build and save the docker image
```shell
docker build -t python-sleep .
docker run python-sleep
docker save python-sleep -o ~/python-sleep.tar # In another session.
```
