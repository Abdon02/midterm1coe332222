# **_Space Exploration provided by the ISS_**

### **_What is this project about?_**
---
This project is about working with Docker containers, Makefiles, API, and Flask by creating the following files: **"app.py"**, **"Dockerfile"**, **"Makefile"**, **"test_app.py"**, **"postion_data.xml"**, **"sighting_data.xml"**. I created a docker image **"abdon02/iss_station:midterm1"** after including all the necessay items inside the **"Dockerfile"**. The container of the docker image had the ability to run nad execute the files from above.

### **_What are each file about?_**
---
- **"app.py"**:
    - This file is a REST API with multiple URL(s) that reads two inputted data files, and returns specific data wanted by the user. The two data files are **"postion_data.xml"** and **"sighting_data.xml"**. The data from the files are stored in two global dictionary variables that will be used throughout the whole program. By using different URL paths, the user is able to request and receive specific data from this Rest API. This is an example of a route used to return data
        ```
        #The purpose of this route: Retuns information on how to interact with the application, (GET)
        @app.route('/', methods=['GET', 'POST'])
        def welcome_message():
            etc...
        ```
- **"position_data.xml"**:
    - This data file is an XML file that contains information about the ISS space station. Here is an example of a data set:
        ```
        <stateVector>
            <EPOCH>2022-042T12:00:00.000Z</EPOCH>
            <X units="km">-4945.2048874258298</X>
            <Y units="km">-3625.9704508659102</Y>
            <Z units="km">-2944.7433487186099</Z>
            <X_DOT units="km/s">1.19203952554952</X_DOT>
            <Y_DOT units="km/s">-5.67286420497775</Y_DOT>
            <Z_DOT units="km/s">4.99593211898374</Z_DOT>
        </stateVector>
            etc ...
        ```
    - You can pull this file from the internet by using this command:
        ```
        wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml
        ```
    - Once you pull this from the internet you will, the file will have a different name. But you can change the name of that file to anything you will like, by doing this command:
        ```
        mv ISS.OEM_J2K_EPH.xml <preferred_name>
        ```
- **"sighting_data.xml"**:
    - This data file is an XML file that contains information about the ISS space station sightings around the world. Here is an example of a data set:
        ```
        <visible_pass><country>Netherlands</country><region>None</region><city>Zeist</city><spacecraft>ISS</spacecraft><sighting_date>Sat Feb 19/07:05 AM</sighting_date><duration_minutes>5</duration_minutes><max_elevation>20</max_elevation><enters>10 above SSW</enters><exits>10 above E</exits><utc_offset>1.0</utc_offset><utc_time>06:05</utc_time><utc_date>Feb 19, 2022</utc_date></visible_pass>
        ect ...
        ```
    - You can pull this file from the internet using this command: 
        ```
        wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesINT04.xml
        ```
    - Once you pull this from the internet you will, the file will have a different name. But you can change the name of that file to anything you will like, by doing this command:
        ```
        mv XMLsightingData_citiesINT04.xml <preferred_name>
        ```
- **"Makefile"**:
    - The purpose of this Makefile was to make the development of this Rest API much faster and cleaner way to debug and change things wrong with the program. Here is a snippet of the file.
        ```
        #This is to build the docker image
        build:
            docker build -t abdon02/iss_station:midterm1 .

        #This is to run the docker image after it was built, without a shell, and also running the server in the background, once we finish running the container it will be deleted from the docker ps list
        run: build
                docker run --name "abemidterm1" -d -p 5036:5000 abdon02/iss_station:midterm1

        #This is to run the docker image after it was built, with a shell, and not running the server in the background
        shell: build
                docker run --rm  -it abdon02/iss_station:midterm1 /bin/bash

        #This is to delete and remove the docker image from docker images and docker ps
        test:
                curl -X GET localhost:5036/
                curl -X POST localhost:5036/data
                curl -X GET localhost:5036/get_epochs
                curl -X GET localhost:5036/get_epochs/2022-057T11:48:56.869Z
                curl -X GET localhost:5036/countries
                curl -X GET localhost:5036/countries/Turkey
                curl -X GET localhost:5036/countries/Turkey/regions
                curl -X GET localhost:5036/countries/Turkey/regions/None
                curl -X GET localhost:5036/countries/Turkey/regions/None/cities
                
        #This is to push the Dockerfile to DockerHub for others to use
            docker push abdon02/iss_station:midterm1
            
        #This is to pull the Dockerfile from DockerHub:
            docker pull abdon02/iss_station:midterm1

        #This is to read the logging displayed by the container
        logging:
                docker logs abdon02/iss_station:midterm1

        #This is to delete the docker image from the docker image list
        delete_images:
                docker rmi abdon02/iss_station:midterm1

        #This is to stop and delete docker containers
        stop:
                docker stop "abemidterm1"
                docker rm "abemidterm1"

        # This is to list out all the images for the name of abdon02
        images:
                docker images -a | grep abdon02

        #This is to list out all the running containers under the name abdon02
        ps:
                docker ps -a | grep abdon02

        ```
    - The way we utilize the Makefile is by using this command: 
        ```
        make <instruction>
        ```
- **"test_app.py"**:
    - This file contains unit tests concerning the functions that were created and used inside the **"app.py"** file. Here is snipped of file:
        ```
        #Testing the function that prints out the welcome message
        def test_welcome_message():
            assert isinstance(welcome_message(), str) == True
        ```
    - To run the test file, it you need to first run the container and interact with it. To do that do this command:
        ```
        docker run --rm  -it abdon02/iss_station:midterm1 /bin/bash
        pytest /code
        
        or 
        
        By using the Makefile, do this command:
            make shell
            pytest /code
        ```
    - The output of running this test should look like this:
        ```
        ======================================== test session starts ========================================
        platform linux -- Python 3.6.8, pytest-7.0.0, pluggy-1.0.0
        rootdir: /code
        collected 1 item

        test_app.py .                                                                                 [100%]

        ========================================= 1 passed in 0.30s =========================================
        ```

### **_How was the Docker image built?_**
---
The Docker image, was built with the help of **"Dockerfile"**. The Dockerfile has "ingredients" and instructions that were going to be needed when we run the container. 
- The following items were added to the container:
    ```
    #The Operating system
    FROM centos:7.9.2009
    
    #To make any updates to the operating system, and download python3
    RUN yum update -y && \
        yum install -y python3

    #To download all the dependies that are used in this project
    RUN pip3 install Flask==2.0.3 \
                    pytest==7.0.0 \
                    xmltodict==0.12.0

    #Attaching all the xml files and other python files into the container
    COPY app.py /code/app.py
    COPY position_data.xml /code/position_data.xml
    COPY sighting_data.xml /code/sighting_data.xml
    COPY test_app.py /code/test_app.py

    WORKDIR /code/
    CMD ["python3","/code/app.py"]
    ```
- To push the Docker file to Docker Hub for others to use. It is important to build the Docker image from the Dockerfile, and then follow the commands bellow: 
    ```
    docker push abdon02/iss_station:midterm1
    
    or 
    
    make push (from the Makefile)
    ```
- You can also pull this DockerFile from DockerHub by using this command:
    ```
    docker pull abdon02/iss_station:midterm1
    
    or 
    
    make pull (from the Makefile)
    ```
- After including all the ingredients for the **"Dockerfile"**, I used the following command to build the Dockerfile into a Docker Image, with a tag "midterm1", and a special name, "abemidterm1". Also, I ran a server in the background so we could test out the Rest API and made sure the routes were returning the correct thing from the inputted request by the user.
    ```
    docker run --name "abemidterm1" -d -p 5036:5000 abdon02/iss_station:midterm1
    ```
    - Or we cound have used the command from the **"Makefile"**:
        ```
        make run
        ```
- After we got the cointer up and running, we would test the Rest API to make sure the URL(s) were working properly. In order to test it fast use this command:
    ```
    make test
    ```
- Once we were done testing the Rest API with the container, and wanted to make more changes. I would stop the container and remove it from the "Docker ps" list that shows all the running containers running on the isp02 machine by using this command:
    ```
    make stop
    ```
### **_Analyzing the results from the API_**
---
After using the **"Makefile"** that was provided above, and running the test to make sure the Rest API was returning the correct information. This would the final outcome cut into pieces: 
```
curl -X GET localhost:5036/
### ISS Tracker 9000 ###
Instructions on how to use this application:
1.- '/'                                                    (GET) prints welcome screen info
2.- '/data'                                                (POST) gathers data from the two files
etc...

curl -X POST localhost:5036/data
Data has been read from the file

curl -X GET localhost:5036/get_epochs
[
  "2022-042T12:00:00.000Z",
  "2022-042T12:04:00.000Z",
  "2022-042T12:08:00.000Z",
  etc...
  
curl -X GET localhost:5036/get_epochs/2022-057T11:48:56.869Z
{
  "EPOCH": "2022-057T11:48:56.869Z",
  "X": {
    "#text": "5150.4217288790296",
    "@units": "km"
  },
  etc...
  
curl -X GET localhost:5036/countries
[
  "Netherlands",
  "New_Caledonia",
  "New_Zealand",
  etc...
  
curl -X GET localhost:5036/countries/Turkey
[
  {
    "city": "Ankara",
    "country": "Turkey",
    "duration_minutes": "3",
    ect...
    
curl -X GET localhost:5036/countries/Turkey/regions
[
  "None"
]

curl -X GET localhost:5036/countries/Turkey/regions/None
[
  {
    "city": "Ankara",
    "country": "Turkey",
    "duration_minutes": "3",
    ect...
    
curl -X GET localhost:5036/countries/Turkey/regions/None/cities
[
  "Ankara"
]
```

You can read what each function returns for each route of this API by doing this command:
```
curl -X GET localhost:5036/
```

## **_Citations_**
---
- Positional Data File:
    ```
    Amazonaws.com, 2022, nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml. Accessed 23 Mar. 2022.
    ```
- Sighting Data File:
    ```
    Amazonaws.com, 2022, nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesINT04.xml. Accessed 23 Mar. 2022.
    ```