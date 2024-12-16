# Search engine benchmark on stack overflow data set

## Introduction
This project compares the performance of three different search engines:
- Elastic Search
- Open Search
- Sphinx

On the StackOverflow dataset available at this link: https://www.brentozar.com/archive/2015/10/how-to-download-the-stack-overflow-database-via-bittorrent/

We could only use the Tiny dataset (1.5 GB) because we lacked of better hardware resources, but one can easily replicate these tests for the bigger datasets.

## How to run it
First of all the dataset comes in msql server, so we've used a container to create a database and load the data in it. 

Once done so we've extracted using an ide (in our case Datagrip) the csv for the tables, Comments, Posts and Users.

Lastly we've moved the csv in a folder data_1 inside this repo.

After that you can create also the folders data_2, data_3 and run 
```sh
python3 csvcut.py
```
which will make sure to generate the scale factors 0.5 and 0.3 respecitvely in folder data_2 and data_3. 

## OpenSearch
In this section we provide the instructions for running a benchmark for search engine database in OpenSearch.
### Initial set up

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

### Credentials used:
- User: ```admin```
- Pass: ```<a123456789A.>```

### Upload data to Opensearch server
For the next step, the server should be running in a docker image.
### Create and Activate virtual environment (recommended)
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

### Install requirements
In this step you will install the the libraries need it to execute the data uploading and the queries.

````bash
pip install -r requirements.txt
````

### Run script and upload data to the OpenSearch server
````bash
python opensearch/upload_data_opensearch.py
````
### Run the query benchmark
- Run the `benchmark_opensearch.ipynb` notebook to get the results of the executions


## Sphinx
The process for Sphinx should be straightforward. First download and install Sphinx and MySQL. The Sphinx binaries should be put in the folder Sphinx. Then run the Python scripts in the following order.
1. mysql.ipynb -- This will load the data files into MySQL and create the indexes for Sphinx
2. sphinx_51_run.ipynb -- This will load Sphinx and run and time all the queries 51 times
3. sphinx_1_run.ipynb -- This will load Sphinx and run and time all the queries 1 time
Note that you could encounter errors if your password and user of MySQL don't match the one precoded in the files. Change that to your convenience. Look also into the sphinx-min.conf.dist file to configure password and user.  

## SQL Server
Finally, if we wanted to compare the results with SQL Server, the easiest way to do it is by downloading and bulk-loading the data from the official webpage mentioned above. Once the data is loaded, it should be enough to run the scripts in the folder called sqlserver.  
## Elasticsearch
You can now start elasticsearch, by running:
```sh
cd elasticsearch
docker compose up
``` 
This will create 3 nodes in a cluster.

### Inserting data in Elastic/Open
For Elasticsearch and Opensearch you can use the same file:
```sh
python3 shared/queries_open_elastic.py
```

Rembember to change the variable **client_to_use**, first to Elasticsearch and then to OpenSearch or viceversa to load to both engines.

Also make sure to have the packages necessary to connect to elastic and opensearch respecively, to install them run:
```sh
pip install elasticsearch opensearch_py
```

### Running the queries in Elastic

To run the queries you can use the notebook **shared/benchmark_open_elastic.ipynb**, again in this case remember to choose the correct client you want to run the queries in (Elastic) by executing one of the respective cells in the **Connecting to Database** section.

The notebook will create the plots, that show how the queries run for all the scalefactors.

## Semantic Search Demo
To run the semantic search demo you can go in the elasticsearch folder and explore the elasticsearch.ipynb file.
Again make sure you've installed the model for creating the embeddings, by running:
```sh
pip install semantic_transformer
```


