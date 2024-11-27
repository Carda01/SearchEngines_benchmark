# advanced_databases_project

## Initial set up

````bash
docker pull opensearchproject/opensearch:2
````
````bash
docker pull opensearchproject/opensearch-dashboards:2
````

````bash
docker pull opensearchproject/opensearch-dashboards:2
````

````bash
docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=a123456789A." opensearchproject/opensearch:latest
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

Check the containers that are running this moment:
```bash
docker container ls
```

Stop the image (put the image ID). Instead of using the command, you can stop the iamge directly in the docker window:
```bash
docker stop <containerId>
```

create and start the containers in detached mode:
```bash
docker-compose up -d
```

Verify that the service containers started correctly:

```bash
docker-compose ps
```

Access to this direction to see the OpenSearch dashboard:
http://localhost:5601/
- User: ```admin```
- Pass: ```<a123456789A.>```



