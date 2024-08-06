import subprocess
import os
import time


def check_docker_running():
    try:
        subprocess.run(["docker", "info"], check=True, stdout=subprocess.DEVNULL)
        print("Docker is running.")
    except subprocess.CalledProcessError:
        print("Docker is not running. Please start Docker and try again.")
        exit(1)


def check_docker_compose_installed():
    try:
        subprocess.run(["docker-compose", "--version"], check=True, stdout=subprocess.DEVNULL)
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


def wait_for_solr_ready(timeout=120):
    print("Waiting for SolrCloud to be ready...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            result = subprocess.run(
                ["docker-compose", "exec", "-T", "solr1", "curl", "-s", "http://localhost:8983/solr/admin/info/system"],
                check=True, capture_output=True, text=True
            )
            if "status" in result.stdout:
                print("SolrCloud is ready.")
                return True
        except subprocess.CalledProcessError:
            pass
        print("Waiting for Solr to start...")
        time.sleep(10)
    print(f"SolrCloud did not become ready within {timeout} seconds.")
    return False


def check_containers_running():
    try:
        result = subprocess.run(["docker-compose", "ps"], check=True, capture_output=True, text=True)
        return "Up" in result.stdout
    except subprocess.CalledProcessError:
        return False


if __name__ == "__main__":
    if not os.path.isfile('docker-compose.yml'):
        print("docker-compose.yml file not found in the current directory.")
        exit(1)

    check_docker_running()
    check_docker_compose_installed()
    deploy_solrcloud()

    if wait_for_solr_ready():
        print("SolrCloud deployment completed successfully.")
    else:
        print("Solr readiness check timed out, but containers might still be starting.")
        if check_containers_running():
            print(
                "Containers are still running. Deployment might be successful, but Solr might need more time to start.")
        else:
            print("Containers are not running. Deployment likely failed.")

    print("Please check Docker Desktop or use 'docker-compose ps' to verify the status of your containers.")

