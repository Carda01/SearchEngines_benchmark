# advanced_databases_project

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
1. If you dont have a folder named `data` in the root directory of this project, create it.
2. Inside the folder, put the `.csv` files with the data.
The basic of list of files need it (there are other in the schema but we are not using all):
- Comments.csv
- Posts.csv
- Users.csv

## Run script and upload data to the OpenSearch server
````bash
python opensearch/upload_data_opensearch.py
````

## Test if everything is okay
- Run the `testing_queries_opensearch.ipynb` notebook to check that it is possible to execute queries.

## What's next?
- With this setup, now each time that you need to execute queries, you only has to run the docker image you created.
- Then connect to the server and the you can execute the queries


