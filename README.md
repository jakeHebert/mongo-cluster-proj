### SUMMARY
This application will allow you to create a sharded MongoDB database and import data from a .csv file into the database. 
The database will be created using docker-compose to containerize and host each service. You will then be able to import data using python.
The database will consist of 3 sharded nodes in a replica set, with 1 node being the primary and the other 2 being secondary, 3 config nodes in a replica set, and 2 mongos routers.



### SETUP AND INSTALLATION
1) Install all dependencies needed.
```
sudo apt install docker
sudo apt install docker-compose
sudo apt install python
sudo apt install git
pip install pymongo
```

Or if you are running this on a clean OS, you may run the setup.sh script after downloading the repo (Step 2).
```
. new-install/setup.sh
```

2) Download this repository and browse to the directory it was placed in.
```
git clone https://github.com/jakeHebert/mongo-csv-import
```

3) Start the application with:
```
docker-compose up
```

4) Configure the dbs to allow them to communicate with each other by running these commands one-by-one:</br>
*NOTE:* After the second command, wait ~30 seconds before running the third.
```
docker exec -it m_cfg1 bash -c "echo 'rs.initiate({_id: \"m_rs1conf\",configsvr: true, members: [{ _id : 0, host : \"m_cfg1\" },{ _id : 1, host : \"m_cfg2\" }, { _id : 2, host : \"m_cfg3\" }]})' | mongo"
docker exec -it m_rs1n1 bash -c "echo 'rs.initiate({_id : \"m_rs1\", members: [{ _id : 0, host : \"m_rs1n1\" },{ _id : 1, host : \"m_rs1n2\" },{ _id : 2, host : \"m_rs1n3\" }]})' | mongo"
docker exec -it m_s1 bash -c "echo 'sh.addShard(\"m_rs1/m_rs1n1\")' | mongo "
```

5) Move a csv file into the app-data for easier access.
```
mv <filename> mongo-csv-import/app-data
```
  Or if the file is on a host machine that needs to be moved to a virtual machine, run this first, then move the file:
```
scp <filename> <username>@<vm ip address>:~/
```

6) Run import.py from the app-data directory:
```
python import.py <"csvfilename.csv">
```

### OTHER INFO AND TROUBLESHOOTING
You may access the database directly by connecting to the mongo router:
```
mongo -port 27019
```
Provided are 2 sample csv files to ensure everything is working properly. sample.csv is a subset of chunk_1.csv, with sample.csv having 298 entries out of the 100000 in chunk_1.csv.</br>
### Sample Queries
Run these queries inside of m_s1:
```
mongo -port 27019
db.myCol.find( {NPPES_PROVIDER_LAST_ORG_NAME:  "CIBULL" } ).pretty()
dby.myCol.aggregate( [
      { $count: "NPPES_PROVIDER_GENDER" }
]).pretty()
```
