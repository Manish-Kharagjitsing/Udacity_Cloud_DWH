Sparkify Cloud Datawarehouse
==============
Note: This project is part of the Udacity Data Engineering Nanodegree program.

Sparkify is a music streaming startup and as part of their growth, they want to move their processes and data onto the cloud. 

In this project, a cloud datawarehouse is build. Source data is stored in an AWS S3 bucket, staged into Redshift and transformed into a star scheme. The star scheme is then used by the Sparkify analytics team to understand user behaviour. 

# Table of Contents
1. [Project Structure](#Project)
2. [Data](#Data)
3. [Staging](#Staging_Tables)
4. [Fact and Dimensional Tables](#Fact_Dim)


# Project Structure <a name="Project"></a>


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

![Alt text](images\Staging_tables.PNG?raw=true "Title")

# Fact and Dimensional Tables <a name="Fact_Dim"></a>

# Technologies <a name="Technologies"></a>

# Install Requirements <a name="Requirements"></a>

