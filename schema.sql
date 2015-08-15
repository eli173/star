
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

create table games (
       id integer primary key autoincrement,
       foreign key(player1) references users(id),
       foreign key(player2) references users(id),
       -- encode board state as a string
       board text
       );
       
       
