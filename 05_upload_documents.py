import csv
import requests
import json

# Configuration
input_file = 'data/Greek_Parliament_Proceedings_1989_2020_DataSample_with_id_and_formatted_date.csv'
solr_url = 'http://localhost:8983/solr/parliamentary_speeches/update'
batch_size = 1000  # Number of documents to send in each batch


# IN CASE OF CLEARING DATA

# delete_url = f"{solr_url}?commit=true"
# delete_query = json.dumps({"delete": {"query": "*:*"}})
# response = requests.post(delete_url, data=delete_query, headers={'Content-type': 'application/json'})
# if response.status_code == 200:
#     print("Successfully deleted all existing documents from Solr")
# else:
#     print(f"Error deleting documents from Solr: {response.text}")


def read_csv_and_send_to_solr(file_path):
    docs = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            docs.append(row)

            if len(docs) >= batch_size:
                send_to_solr(docs)
                docs = []

    # Send any remaining documents
    if docs:
        send_to_solr(docs)


def send_to_solr(docs):
    headers = {'Content-type': 'application/json'}
    data = json.dumps(docs)
    response = requests.post(solr_url, data=data, headers=headers)
    if response.status_code == 200:
        print(f"Successfully sent {len(docs)} documents to Solr")
    else:
        print(f"Error sending documents to Solr: {response.text}")


# Main execution
if __name__ == "__main__":
    read_csv_and_send_to_solr(input_file)

    # Commit the changes
    commit_url = f"{solr_url}?commit=true"
    response = requests.get(commit_url)
    if response.status_code == 200:
        print("Successfully committed changes to Solr")
    else:
        print(f"Error committing changes to Solr: {response.text}")
