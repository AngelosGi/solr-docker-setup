import subprocess
import sys


def upload_config_to_zookeeper(config_name="myconfig"):
    try:
        print(f"Uploading configuration '{config_name}' to ZooKeeper...")
        result = subprocess.run(
            ["docker-compose", "exec", "-T", "solr1", "solr", "zk", "upconfig", "-n", config_name,
             "-d", f"/opt/solr/server/solr/configsets/{config_name}"],
            check=True, capture_output=True, text=True
        )
        print(f"Configuration '{config_name}' uploaded successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error uploading configuration to ZooKeeper: {e}")
        print(f"Error output: {e.stderr}")
        return False


if __name__ == "__main__":
    config_name = "myconfig"
    if len(sys.argv) > 1:
        config_name = sys.argv[1]

    if upload_config_to_zookeeper(config_name):
        print("Configuration upload completed successfully.")
    else:
        print("Failed to upload configuration.")
        sys.exit(1)




