
drop table if exists users;
drop table if exists games;

create table users (
       id integer primary key autoincrement,
       username text not null,
       pw_hash text not null,
       wins integer default 0,
       losses integer default 0
       );

create table games (
       id integer primary key autoincrement,
       -- encode board state as a string
       board text not null,
       player1 integer,
       player2 integer,
       foreign key(player1) references users(id),
       foreign key(player2) references users(id)
       );
       
       
