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

#This is to push the docker image up to Docker Hub
push:
	docker push abdon02/iss_station:midterm1

#This is to pull the docker image from DockerHub
pull:
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




