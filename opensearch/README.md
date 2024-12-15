# Search engine benchmark for OpenSearch
In this section we provide the instructions for running a benchmark for search engine database in OpenSearch. The data used correspond to Stackover flow tiny database: https://www.brentozar.com/archive/2015/10/how-to-download-the-stack-overflow-database-via-bittorrent/

## Initial set up

````bash
docker pull opensearchproject/opensearch:2
````


````bash
docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=<a123456789A.>" opensearchproject/opensearch:latest
````

Using bash (Git Bash), run this command to check if the image is running
````bash
curl https://localhost:9200 -ku admin:"<a123456789A.>"
````

If you get something like this, is okay:

````
{
  "name" : "4f2e9348a9be",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "Y2hwrChZQCOEMl-j0BF45Q",
  "version" : {
    "distribution" : "opensearch",
    "number" : "2.18.0",
    "build_type" : "tar",
    "build_hash" : "99a9a81da366173b0c2b963b26ea92e15ef34547",
    "build_date" : "2024-10-31T19:08:39.157471098Z",
    "build_snapshot" : false,
    "lucene_version" : "9.12.0",
    "minimum_wire_compatibility_version" : "7.10.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "The OpenSearch Project: https://opensearch.org/"
}
````

## Credentials used:
- User: ```admin```
- Pass: ```<a123456789A.>```

# Upload data to Opensearch server
For the next step, the server should be running in a docker image.
## Create and Activate virtual environment (recommended)
It is highly recommended to create a virtual enviroment and the activate it.

Create Virtual environment:
````bash
python -m venv myenv
````

Activate Virtual environment:
````bash
./venv/Scripts/activate
````

- This command were use in windows. If those command doesn't work, look for the corrects ones according to the terminal you are using or OS (mac, linux, etc)

## Install requirements
In this step you will install the the libraries need it to execute the data uploading and the queries.

````bash
pip install -r requirements.txt
````


## Set up data files
1. First, you have to create three folder in the root directory for saving the data: `data_1`, `data_2`, `data_3`
you can use the next command line:
````bash
mkdir data_1
````
````bash
mkdir data_2
````
````bash
mkdir data_3
````
2. Inside the folder `data_1`, put the `.csv` files with the data.
The basic of list of files need it (there are other in the schema but we are not using all):
- Comments.csv
- Posts.csv
- Users.csv

## Run script to create the other scales factor
This script take the original data inside the `data_1` folder and generates the scales factor 0.5 (`data_2`) and 0.3 (`data_3`)

````bash
python csvcut.py
````

## Run script and upload data to the OpenSearch server
````bash
python opensearch/upload_data_opensearch.py
````

## Run the query benchmark
- Run the `benchmark_opensearch.ipynb` notebook to get the results of the executions

