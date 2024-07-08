# OpenAgri EntryPoint
This repository serves as a easy to use entry point, with a modular configuration and deployment of the OpenAgri services.

# Dependencies
This project depends on docker (version > 20.10.0) and Python (2 or 3).

# Setup
1. Copy any service YAML (.yml) file from the `available_services` directory into the `services_in_use` directory.
2. Copy the `example.env` to a new file called `.env`. In this new file change the configurations of the selected services to meet your deployment scenario. We strongly suggest changing configurations for the default usernames and passwords of the services used.

# Running
To run all, execute the following command:
```
$ python run_compose.py [docker_compose_commands]
```
replacing `[docker_compose_commands]` with the actual docker compose command you wish to use.

Bellow is a list of examples:
## Update Local Docker Images
Update images from all services listed on `services_in_use`:
```
$ python run_compose.py pull
```
Update the image of only a single service (e.g., gatekeeper):

```
$ python run_compose.py pull gatekeeper
```

## Starting Services in Background
Start in background all services listed on `services_in_use`:
```
$ python run_compose.py up -d
```
Start in background only a single service (e.g., gatekeeper):
```
$ python run_compose.py up -d gatekeeper
```

## Tearing Down Services
Stop and remove containers from all services listed on `services_in_use`:
```
$ python run_compose.py down
```
Stop and remove container of only a single service (e.g., gatekeeper):
```
$ python run_compose.py down gatekeeper
```


## Start/Stop Services
To stop all running container (without removing it):
```
$ python run_compose.py stop
```
To stop a specific running container (without removing it) (e.g., gatekeeper):
```
$ python run_compose.py stop gatekeeper
```

Similarly, to start all stopped container:
```
$ python run_compose.py start
```
or if re-starting a specific service(e.g., gatekeeper)
```
$ python run_compose.py start gatekeeper
```

# License
This project code is licensed under the EUPL 1.2 license, see the LICENSE file for more details.
Please note that each service may have different licenses, which can be found their specific source code repository.