drop table if exists user;
create table user (
    id integer primary key autoincrement,
    username text not null,
    password text not null,
    noticenum integer not null default 0,
    notification text
);

drop table if exists tv;
create table tv (
    id integer primary key autoincrement,
    tvname text not null,
    episode integer not null,
    epname text,
    address text not null,
    type text not null
);

drop table if exists ping;
create table ping (
    id integer primary key autoincrement,
    name text not null,
    time integer not null,
    episode text not null,
    address text not null
);

drop table if exists discuss;
create table discuss (
    id integer primary key autoincrement,
    tvname text not null,
    name1 text not null,
    name2 text,
    replyid integer,
    time integer not null,
    warning integer not null,
    level integer not null default 0,
    content text not null
);

drop table if exists dream;
create table dream (
    id integer primary key autoincrement,
    name text not null,
    imgsrc text,
    enname text,
    link_youku text,
    link_iqiyi text,
    link_vqq text
);

drop table if exists tracking;
create table tracking (
    id integer primary key autoincrement,
    tvname text not null,
    userid integer not null,
    epnum integer not null default 0,
    end integer not null default 0
);

drop table if exists notification;
create table notification (
    id integer primary key autoincrement,
    username text not null,
    userid integer not null,
    content integer not null default 0,
    link integer not null default 0
);