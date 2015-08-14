
drop table if exists users;
drop table if exists games;

create table users (
       id integer primary key autoincrement,
       username text not null,
       salt text not null,
       hash text not null,
       wins integer,
       losses integer
       );
