# SolrCloud Parliamentary Speeches Setup

This project sets up a SolrCloud environment for indexing and searching parliamentary speeches. It can be adapted for other datasets with similar structures. This guide provides detailed, step-by-step instructions for setup, use, and customization.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [File Structure](#file-structure)
3. [Detailed Setup Instructions](#detailed-setup-instructions)
4. [Adapting for Different Datasets](#adapting-for-different-datasets)
5. [Troubleshooting](#troubleshooting)
6. [Maintenance and Management](#maintenance-and-management)

## Prerequisites

Ensure you have the following installed on your system:
- Docker (version 19.03 or later)
- Docker Compose (version 1.25 or later)
- Python 3.7 or later
- pip (Python package installer)

Install the required Python libraries:
```bash
pip install requests
```

## File Structure

Ensure your project directory is structured as follows:
```
project_root/
│
├── 01_deploy_solr.py
├── 02_upload_config.py
├── 03_create_collection.py
├── 04_upload_documents.py
├── 05_stop_and_clean.py
├── docker-compose.yml
├── configsets/
│   └── myconfig/
│       ├── schema.xml
│       └── solrconfig.xml
└── data/
    └── Greek_Parliament_Proceedings_1989_2020_DataSample_with_id_and_formatted_date.csv
```

## Detailed Setup Instructions

Follow these steps carefully to set up and run your SolrCloud environment:

### Step 1: Deploy SolrCloud

1. Open a terminal and navigate to your project root directory.
2. Run the deployment script:
   ```bash
   python 01_deploy_solr.py
   ```
3. The script will:
   - Check if Docker is running
   - Verify Docker Compose is installed
   - Start the SolrCloud containers defined in `docker-compose.yml`
   - Wait for SolrCloud to be ready (this may take a few minutes)

4. If successful, you'll see the message: "SolrCloud deployment completed successfully."

### Step 2: Upload Configuration

1. In the same terminal, run:
   ```bash
   python 02_upload_config.py myconfig
   ```
2. This script uploads the configuration files from `configsets/myconfig/` to ZooKeeper.
3. If successful, you'll see: "Configuration 'myconfig' uploaded successfully."

### Step 3: Create Collection

1. Create a new collection by running:
   ```bash
   python 03_create_collection.py parliamentary_speeches
   ```
2. This creates a new collection named "parliamentary_speeches" using the uploaded configuration.
3. If successful, you'll see: "Collection 'parliamentary_speeches' created successfully."

### Step 4: Upload Documents

1. Before running the upload script, ensure your CSV file is in the correct location and format.
2. Run the upload script:
   ```bash
   python 04_upload_documents.py
   ```
3. This script will read the CSV file and upload the documents to Solr in batches.
4. You'll see progress messages like: "Successfully sent X documents to Solr"
5. At the end, it will commit the changes to Solr.

### Step 5: Verify Setup

1. Open a web browser and go to `http://localhost:8983/solr/`
2. You should see the Solr Admin interface.
3. Click on "Core Selector" and choose "parliamentary_speeches"
4. Go to the "Query" section and click "Execute Query" to see if your documents are indexed.

## Adapting for Different Datasets

To use this setup with a different dataset, you'll need to modify several files:

### 1. Modify schema.xml

1. Open `configsets/myconfig/schema.xml`
2. Update the `<fields>` section to match your data structure:
   - Add, remove, or modify `<field>` elements
   - Ensure the `name` attribute matches your CSV column names
   - Choose appropriate `type` attributes (e.g., "string", "text_general", "date")
3. Adjust `<copyField>` directives if needed
4. Change the `<uniqueKey>` if your unique identifier field is different

Example field definition:
```xml
<field name="your_field_name" type="text_general" indexed="true" stored="true"/>
```

### 2. Update 04_upload_documents.py

1. Open `04_upload_documents.py`
2. Change the `input_file` path to your CSV file:
   ```python
   input_file = 'data/your_new_data.csv'
   ```
3. Modify the `solr_url` if you used a different collection name:
   ```python
   solr_url = 'http://localhost:8983/solr/your_collection_name/update'
   ```
4. Adjust the CSV parsing logic if your file structure is different:
   ```python
   reader = csv.DictReader(file)
   for row in reader:
       # Modify this part to match your CSV structure
       doc = {
           'id': row['your_id_field'],
           'field1': row['your_field1'],
           'field2': row['your_field2'],
           # ... add all your fields here
       }
       docs.append(doc)
   ```

### 3. Adjust docker-compose.yml (if needed)

1. Open `docker-compose.yml`
2. If you changed the config name, update the volume mapping:
   ```yaml
   volumes:
     - ./configsets/your_config_name:/opt/solr/server/solr/configsets/your_config_name
   ```
3. Modify port mappings if needed (e.g., if port 8983 is already in use)

### 4. Update 03_create_collection.py

1. Open `03_create_collection.py`
2. Change the default `config_name` if you used a different name:
   ```python
   config_name = "your_config_name"
   ```

After making these changes, follow the setup instructions again from Step 1.

## Troubleshooting

If you encounter issues:

1. **SolrCloud fails to start:**
   - Check Docker logs: `docker-compose logs`
   - Ensure all required ports are available
   - Verify Docker and Docker Compose versions

2. **Configuration upload fails:**
   - Check ZooKeeper connectivity
   - Ensure config files are in the correct location

3. **Collection creation fails:**
   - Verify the config was uploaded successfully
   - Check Solr logs for any error messages

4. **Document upload fails:**
   - Verify your CSV structure matches the schema
   - Check for any data formatting issues
   - Ensure Solr is running and the collection exists

5. **Query returns no results:**
   - Verify documents were uploaded successfully
   - Check your query syntax
   - Ensure you're querying the correct fields

## Maintenance and Management

1. **Stopping the System:**
   To stop and remove the SolrCloud containers and clean up data:
   ```bash
   python 05_stop_and_clean.py
   ```

2. **Backing Up Data:**
   - Use Solr's backup API or
   - Create a snapshot of the data directory

3. **Monitoring:**
   - Use Solr's admin interface for basic monitoring
   - Consider setting up Prometheus and Grafana for advanced monitoring

4. **Scaling:**
   - Add more Solr nodes in the `docker-compose.yml` file
   - Increase the number of shards when creating the collection

Remember to adjust security settings and add authentication for production deployments. This setup is intended for development and testing purposes.