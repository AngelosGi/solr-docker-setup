import requests
import sys


def create_collection(collection_name, config_name, num_shards=1, replication_factor=1):
    print(f"Creating collection '{collection_name}'...")
    create_url = f"http://localhost:8981/solr/admin/collections?action=CREATE&name={collection_name}&numShards={num_shards}&replicationFactor={replication_factor}&collection.configName={config_name}&wt=json"

    try:
        response = requests.get(create_url)
        response_json = response.json()

        if response.status_code == 200 and response_json.get('responseHeader', {}).get('status') == 0:
            print(f"Collection '{collection_name}' created successfully.")
            return True
        else:
            print(f"Failed to create collection. Response: {response.text}")
            return False
    except requests.RequestException as e:
        print(f"Error creating collection: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("How to Use: \npython create_collection.py <collection_name>")
        sys.exit(1)

    collection_name = sys.argv[1]
    config_name = "myconfig"
    num_shards = 1
    replication_factor = 1

    if create_collection(collection_name, config_name, num_shards, replication_factor):
        print("Collection creation process completed.")
    else:
        print("Failed to create collection.")


if __name__ == "__main__":
    main()

# run python create_collection.py <collection_name>
