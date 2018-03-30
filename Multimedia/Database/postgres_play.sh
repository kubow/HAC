#source http://blog.jasonmeridth.com/posts/postgresql-command-line-cheat-sheet/
sudo -u postgres psql 
#list databases
\l
#list roles
\du
#create role CREATE ROLE demorole1 WITH LOGIN ENCRYPTED PASSWORD 'password1' CREATEDB;
#alter role ALTER ROLE demorole1 CREATEROLE CREATEDB REPLICATION SUPERUSER;
ALTER ROLE postgres WITH PASSWORD 'Aaa123456';
#drop role DROP ROLE demorole1;
#create database CREATE DATABASE demodb1 WITH OWNER demorole1 ENCODING 'UTF8';
#grant privileges to new user GRANT ALL PRIVILEGES ON DATABASE demodb1 TO demorole1;
#drop database DROP DATABASE demodb1;
#connect to database \c <databasename>
#list tables in connected database \dt
#list columns on table \d <tablename>
#backup database 
pg_dump <databasename> > <outfile>
