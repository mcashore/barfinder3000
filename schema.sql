drop table if exists bars;
/*create table bars (
  id integer primary key autoincrement,
  name string not null,
  latitude integer not null,
  longitude integer not null,
  cheapest_drink_id integer
);*/

drop table if exists drinks;
/*
create table drinks (
  id integer primary key autoincrement,
  name string not null,
  bar_id integer not null,
  category integer,
  age_group integer
);*/

drop table if exists drink_deals;
create table drink_deals (
  id integer primary key autoincrement,
  day integer not null,
  drink_cost real not null,
  drink_name string not null,
  drink_category integer,
  bar_name string not null,
  bar_lat real not null,
  bar_lon real not null
);