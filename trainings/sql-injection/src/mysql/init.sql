create database if not exists db;
use db;
create table if not exists fl4g(username varchar(32), password varchar(32));
insert into fl4g values('rooot', 'fake flag');
insert into fl4g values('root', 'flag{sql-injection}');