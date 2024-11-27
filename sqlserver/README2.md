# Set up SQL server container

The instructions come from this tutorial: https://www.brentozar.com/archive/2023/01/how-to-install-sql-server-and-the-stack-overflow-database-on-a-mac/
## Step 0: Get SQL server container

```bash
docker pull mcr.microsoft.com/mssql/server:2022-latest
```

```bash
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=<YourStrong@Passw0rd>" \
   -p 1433:1433 --name sqlserver_se --hostname sql1 \
   -d \
   mcr.microsoft.com/mssql/server:2022-latest
```

## Step 1: Download and restore Stackoverflow Database
In the following steps, we download the Stack Overflow Mini database ~1GB version.

Create the folder `data`.
```bash
mkdir data
```
Move to the `data` folder.
```bash
cd data/
```
Download the `StackOverflowMini.bak` and save in the data folder. (This could take some minutes)
```bash
curl -L -o StackOverflowMini.bak 'https://github.com/BrentOzarULTD/Stack-Overflow-Database/releases/download/20230114/StackOverflowMini.bak'
```
Move the `.bak` file into the SQL server container
```bash
docker cp StackOverflowMini.bak sqlserver_se:/var/backups
```
Check if the file it is inside the container directory (Optional but recommend it)

```bash
docker exec -it sqlserver_se bash
```

```bash
cd /var/backups
```

```bash
ls -l
```

```bash
exit
```
If after running those commands you see the `StackOverflowMini.bak`, everything is Okay :) . Otherwise, check the previous steps.

## Step 2: Create the database in SQLserver

For this step you need to have installed Microsoft SQL Server Management Studio (SSMS). If you don't have it download and install it:

1) [Download SSMS](https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver16) and install it.
2) Open SSMS and connect to the server. Remember, the docker image should be running.
Use this configuration:
   - Server type: Database Engine
   - Server name: 127.0.0.1 (if it doesn't work try 'localhost')
   - Authentication: SQL Server Authentication
   - Login: `sa`
   - Password: `<YourStrong@Passw0rd>` (the password you set before)
   - Encryption: Mandatory
   - Trust server certificate
3) Once connected, open a SQL script (for example, press in the "New query") and execute:
```sql
RESTORE DATABASE StackOverflowMini FROM DISK='/var/backups/StackOverflowMini.bak'
WITH MOVE 'StackOverflowMini' TO '/var/opt/mssql/data/StackOverflowMini.mdf', 
MOVE 'StackOverflowMini_log' TO '/var/opt/mssql/data/StackOverflowMini_log.ldf';
GO
```
That last code restore the `StackOverflowMini` database and now the data will be able in the server. In the Database folder
on the left, you should see `StackOverflowMini`.

# Testing queries executions

Once setting up the database, now you can test some queries.
## Step 0 (recommended): create a virtual enviroment 

## Step 0.1: Install the requirements:
```commandline
pip install -r requirements.txt
```

## Step 1:
Execute the `testing_queries` notebook. This notebook takes the testing queries defined in `src/queries.py`, and then
run them to measure the executing time.








