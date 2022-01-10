Sparkify Cloud Datawarehouse
==============
Note: This project is part of the Udacity Data Engineering Nanodegree program.

Sparkify is a music streaming startup and as part of their growth, they want to move their processes and data onto the cloud. 

In this project, a cloud datawarehouse is build. Source data is stored in an AWS S3 bucket, staged into Redshift and transformed into a star scheme. The star scheme is then used by the Sparkify analytics team to understand user behaviour. 

# Table of Contents
1. [Project Readme](#run)
2. [Structure](#Project)
3. [Data](#Data)
4. [Staging](#Staging_Tables)
5. [Fact and Dimensional Tables](#Fact_Dim)


# Project Readme <a name="run" ></a>
## Software Requirements 
Python Packages: 
- boto3
- json 
- Configparser 
- psycopg2

## Scripts 
The scripts should be run in the following order: 

1. dwh.cfg 

This file contains the AWS parameter credentials. Also, the parameters for the redshift clusters are defined. 

2. create_red_cluster.py

This script creates the redshift cluster in AWS. The parameters for the cluster are defined in the dwh.cfg file. 

3. test.py

By running this file, it can be seen whether or not the aws redshift cluster is succesfully setup. 

4. sql_queries.py

All the queries are defined in this file. 

5. create_tables.py

This script creates the tables in the databases in the redshift cluster. 

6. etl.py

The data is loaded into the staging tables and then into the star scheme. 

7. drop_redshift_cluster.py

By running this script, the redshift cluster is dropped. 
   




# Structure <a name="Project"></a>


The purpose of this project is to demonstrate the value of the cloud data warehouse for the music streaming app. Log data and song data is stored in an AWS S3 Bucket and will eventually be loaded and transformed into a star scheme in a AWS Redshift Cluster. 



# Data <a name="Data"></a>

## Song Dataset 

```
{"song_id": "SOBLFFE12AF72AA5BA", "num_songs": 1, "title": "Scream", "artist_name": "Adelitas Way", "artist_latitude": null, "year": 2009, "duration": 213.9424, "artist_id": "ARJNIUY12298900C91", "artist_longitude": null, "artist_location": ""}
```

## Log Dataset 
```
{'artist': 'Muse', 'auth': 'Logged In', 'firstName': 'Harper', 'gender': 'M', 'itemInSession': 1, 'lastName': 'Barrett', 'length': 209.50159, 'level': 'paid', 'location': 'New York-Newark-Jersey City, NY-NJ-PA', 'method': 'PUT', 'page': 'NextSong', 'registration': 1540685364796.0, 'sessionId': 275, 'song': 'Supermassive Black Hole (Twilight Soundtrack Version)', 'status': 200, 'ts': 1541721977796, 'userAgent': '"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"', 'userId': '42'}
```

# Staging Tables <a name="Staging_Tables"></a>
The data in the song and log files files stored in the S3 bucket /udacity-dend/ are copied into the staging tables S_events and S_songs. 


![Alt text](images/Staging_tables.PNG?raw=true "Title")


# Fact and Dimensional Tables <a name="Fact_Dim"></a>
The star scheme can be seen in the figure below. The fact table is named with an 'F_{fact name}' . Dimensional tables are named as 'D_{dimension name}'. 

![Alt text](images/StarScheme_tables.PNG?raw=true "Title")



