import subprocess
import os


def check_docker_compose_installed():
    try:
        subprocess.run(["docker-compose", "--version"], check=True)
        print("Docker Compose is installed.")
    except subprocess.CalledProcessError:
        print("Docker Compose is not installed or not found in PATH.")
        exit(1)


def deploy_solrcloud():
    try:
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        print("SolrCloud deployment started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while deploying SolrCloud: {e}")
        exit(1)


if __name__ == "__main__":
    # Check if docker-docker-compose.yml exists in the current directory
    if not os.path.isfile('docker-compose.yml'):
        print("docker-docker-compose.yml file not found in the current directory.")
        exit(1)

    # Ensure docker-compose is available
    check_docker_compose_installed()

    # Deploy SolrCloud
    deploy_solrcloud()
