
drop table if exists users;
drop table if exists games;
drop table if exists waiting;

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
       board text not null default "00000000000000000000000000000000000000000000000000",
       whose_turn integer, -- 0 or 1 for p1 or p2... confusing?
       player1 integer,
       player2 integer,
       p1done integer default 0, -- zero if continuing
       p2done integer default 0, -- zero if continuing
       foreign key(player1) references users(id),
       foreign key(player2) references users(id)
       );
       
       
create table waiting (
       id integer primary key autoincrement,
       player integer,
       seeking integer,
       foreign key(player) references users(id),
       foreign key(seeking) references users(id)
       );
