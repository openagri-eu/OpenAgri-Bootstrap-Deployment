#!/usr/bin/env python
import glob
import os
import subprocess
import sys



SERVICE_LOCAL_PORT_MAPPING_TEMPLATE = """
    {service_name}:
        ports:
            - "${{{service_port}}}:${{{service_port}}}"
"""

SERVICE_FILE_NAMES_TO_SERVICE_NAME = {
    'irrigationservice.yml': 'irrigation',
    'pestmanagement.yml': 'pdm',
    'weatherservice.yml': 'weathersrv',
}

SERVICE_NAMES_TO_PORT_ENV_VARS = {
    "gatekeeper": 'GATEKEEPER_APP_PORT',
    "farmcalendar": 'FARM_CALENDAR_APP_PORT',
    "pdm": 'PDM_SERVICE_PORT',
    "weathersrv": 'WEATHER_SRV_PORT',
    "irrigation": 'IRR_SERVICE_PORT',
    "reporting": 'REPORTING_SERVICE_PORT',
}


def create_override_file_if_not_exist(file_path, extra_content=None):

    should_create_file = not os.path.exists(file_path)
    if not should_create_file:
        user_confirm = input('You are about to overwrite the existing override file. Do you want to continue? (y/[n]): ')
        if user_confirm.lower() == 'y':
            should_create_file = True

    if should_create_file:
        print(f"Creating override file: {file_path}")
        with open(file_path, 'w') as f:
            f.writelines([
                'services:', '\n'
            ])
            if extra_content is not None:
                f.write(extra_content)
        return True
    return False


def deploy_localhost(override_compose_file, service_in_use_files):
    extra_content = ""
    for service_file_path in service_in_use_files:
        file_name = os.path.basename(service_file_path)
        service_name = SERVICE_FILE_NAMES_TO_SERVICE_NAME.get(file_name, file_name.split('.')[0])
        service_port = SERVICE_NAMES_TO_PORT_ENV_VARS.get(service_name)
        if service_port is None:
            raise Exception(f"Warning: No port mapping found for service '{service_name}'.")
        extra_content += SERVICE_LOCAL_PORT_MAPPING_TEMPLATE.format(service_name=service_name, service_port=service_port)
    if create_override_file_if_not_exist(override_compose_file,  extra_content=extra_content):
        print("Override file created successfully.")


def handle_deploy_command(argv, override_compose_file, service_in_use_files):
    if argv[0] == "deploy-localhost":
        deploy_localhost(override_compose_file, service_in_use_files)
        return True

    return False


def main():
    # Set the main docker-compose file
    main_compose_file = "docker-compose.yml"
    override_compose_file = "docker-compose.override.yml"

    services_dir = "services_in_use"
    service_in_use_files = glob.glob(os.path.join(services_dir, "*.yml"))
    if handle_deploy_command(sys.argv[1:], override_compose_file, service_in_use_files):
        # exists if used our deploy-localhost command
        # we don't want to pass this to docker compose
        return

    compose_files = [main_compose_file] + service_in_use_files + [override_compose_file]

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
