# SolrCloud Docker Setup

This project provides a Docker-based setup for SolrCloud 9.6.1 with scripts to manage deployment, collection creation, and cleanup.

## Overview

The project includes:
- A Docker Compose file for setting up a SolrCloud cluster
- Python scripts for deploying, creating collections, and cleaning up the environment
- Configuration files for Solr (schema.xml and solrconfig.xml)

## Prerequisites

- Docker and Docker Compose
- Python 3.x
- `requests` Python library (`pip install requests`)

## Setup

1. Clone this repository:
   ```
   https://github.com/AngelosGi/solr-docker-setup.git
   git@github.com:AngelosGi/solr-docker-setup.git
   cd solr-docker-setup
   ```

2. Ensure your Solr configuration files (schema.xml and solrconfig.xml) are in the `configsets/myconfig/conf/` directory.

## Usage

### Deploying SolrCloud

To deploy the SolrCloud cluster:

```
python 01_deploy_solr.py
```

This script will:
- Check if Docker and Docker Compose are installed
- Start the SolrCloud containers x3
- Start the Zookeper containers x3

### Uploading Solrconfig set

To upload the configset :

```
python 02_upload_config.py
OR python upload_config.py <config_name>
```

### Creating a Collection

To create a new collection:

```
python create_collection.py <collection_name>
```

Replace `<collection_name>` with your desired collection name.

### Cleaning Up

To stop the containers and clean up the environment:

```
python cleanup_solr.py
```

This script will:
- Stop and remove the Docker containers
- Remove Solr and ZooKeeper data directories

## Configuration

- `docker-compose.yml`: Defines the SolrCloud and ZooKeeper services
- `configsets/myconfig/conf/schema.xml`: Defines the schema for your Solr collections
- `configsets/myconfig/conf/solrconfig.xml`: Configures Solr behavior

## Customization

- Modify `schema.xml` and `solrconfig.xml` to adjust Solr configuration
- Edit the Python scripts to change default parameters (e.g., number of shards, replication factor)

## Troubleshooting

- If you encounter issues, check the Docker logs:
  ```
  docker-compose logs
  ```
- Ensure all required ports are available (8981, 8982, 8983 for Solr; 2181, 2182, 2183 for ZooKeeper)

## Contributing

Contributions to improve the scripts or documentation are always welcome.

```
