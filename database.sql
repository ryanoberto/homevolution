drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);

drop table if exists slaves;
create table slaves (
  id integer primary key autoincrement,
  node text not null,
  key text not null
);

drop table if exists devices;
create table devices (
  id integer primary key autoincrement,
  name text not null,
  mac text not null
);

drop table if exists kodi;
create table kodi (
  id integer primary key autoincrement,
  name text not null
);

drop table if exists zoneminder;
create table zoneminder (
  id integer primary key autoincrement,
  name text not null,
  url text not null
);
