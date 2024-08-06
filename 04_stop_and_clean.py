import subprocess
import os


def check_docker_compose_installed():
    try:
        subprocess.run(["docker-compose", "--version"], check=True, stdout=subprocess.DEVNULL)
        print("Docker Compose is installed.")
    except subprocess.CalledProcessError:
        print("Docker Compose is not installed or not found in PATH.")
        exit(1)


def stop_and_remove_containers():
    try:
        print("Stopping and removing containers...")
        subprocess.run(["docker-compose", "down", "-v"], check=True)
        print("Containers stopped and removed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while stopping containers: {e}")
        exit(1)


def remove_solr_data():
    data_dir = "./solr_data"  # Adjust this path if your Solr data is stored elsewhere
    if os.path.exists(data_dir):
        try:
            print(f"Removing Solr data directory: {data_dir}")
            subprocess.run(["rm", "-rf", data_dir], check=True)
            print("Solr data removed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while removing Solr data: {e}")
            exit(1)
    else:
        print(f"Solr data directory not found: {data_dir}")


def clean_zookeeper_data():
    zk_data_dir = "./zk_data"  # Adjust this path if your ZooKeeper data is stored elsewhere
    if os.path.exists(zk_data_dir):
        try:
            print(f"Removing ZooKeeper data directory: {zk_data_dir}")
            subprocess.run(["rm", "-rf", zk_data_dir], check=True)
            print("ZooKeeper data removed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while removing ZooKeeper data: {e}")
            exit(1)
    else:
        print(f"ZooKeeper data directory not found: {zk_data_dir}")


if __name__ == "__main__":
    check_docker_compose_installed()
    stop_and_remove_containers()
    remove_solr_data()
    clean_zookeeper_data()
    print("Cleanup completed successfully.")

