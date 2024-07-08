#!/usr/bin/env python
import os
import subprocess
import sys

def main():
    # Set the main docker-compose file
    main_compose_file = "docker-compose.yml"

    services_dir = "services_in_use"

    compose_files = [main_compose_file]

    for service_file in os.listdir(services_dir):
        if service_file.endswith(".yml"):
            compose_files.append(os.path.join(services_dir, service_file))

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