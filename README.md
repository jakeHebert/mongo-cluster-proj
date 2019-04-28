1) Install Docker and docker-compose
```
sudo apt install docker
sudo apt install docker-compose
```
2) Download this repository and browse to the directory it was placed in.
3) Start the application with:
```
docker-compose up
```
4) Configure the dbs to allow them to communicate with each other by running these commands one-by-one:
```
docker exec -it mongocfg1 bash -c "echo 'rs.initiate({_id: \"mongors1conf\",configsvr: true, members: [{ _id : 0, host : \"mongocfg1\" },{ _id : 1, host : \"mongocfg2\" }, { _id : 2, host : \"mongocfg3\" }]})' | mongo"
docker exec -it mongors1n1 bash -c "echo 'rs.initiate({_id : \"mongors1\", members: [{ _id : 0, host : \"mongors1n1\" },{ _id : 1, host : \"mongors1n2\" },{ _id : 2, host : \"mongors1n3\" }]})' | mongo"
 docker exec -it mongos1 bash -c "echo 'sh.addShard(\"mongors1/mongors1n1\")' | mongo "
```
4.5) (Optional) Move a csv file into the app-data for easier access.
5) Run import.py from the app-data directory:
```
python import.py <"csvfilename.csv">
```
