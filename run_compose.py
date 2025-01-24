#!/usr/bin/env python
import os
import subprocess
import sys


def create_override_file_if_not_exist(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.writelines(["version: '3.9'", ''])


def main():
    # Set the main docker-compose file
    main_compose_file = "docker-compose.yml"
    override_compose_file = "docker-compose.override.yml"
    create_override_file_if_not_exist(override_compose_file)

    services_dir = "services_in_use"

    compose_files = [main_compose_file]

    for service_file in os.listdir(services_dir):
        if service_file.endswith(".yml"):
            compose_files.append(os.path.join(services_dir, service_file))

    compose_files.append(override_compose_file)

    compose_command = ["docker", "compose"]
    for compose_file in compose_files:
        compose_command.extend(["-f", compose_file])

    compose_command.extend(sys.argv[1:])

    # Print the constructed command (for debugging purposes)
    print("Running command:", " ".join(compose_command))

    # Run the docker compose command
    subprocess.run(compose_command)

if __name__ == "__main__":
    main()