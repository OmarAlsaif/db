drop table if exists bus_info CASCADE;
drop table if exists bus_stop CASCADE;
drop table if exists drivers CASCADE;
drop table if exists travelers CASCADE;
drop table if exists trip_info CASCADE;
drop table if exists bookings CASCADE;

create table bus_info (
id                  integer,
departure_des       text,
arrival_des         text,
primary key (id));

create table bus_stop (
bus_id              integer,
country             text,
city                text,
street_name         varchar(45),
primary key (bus_id),
foreign key (bus_id) references bus_info(id));

create table drivers (
driver_id           integer,
ss_nr               varchar(12),
driver_name         varchar(50),
street_name         varchar(45),
phone_nr            varchar(16),
primary key (driver_id));

create table travelers (
id                  integer,
prn_name            varchar(50),
street_name         varchar(45),
email               varchar(100),
phone_nr            varchar(16),
primary key (id));

create table trip_info (
trip_id             serial,
bus_id              integer,
da_te               date,
departure_time      time,
arrival_time        time,
price               numeric,
seating             numeric,
driver_id           integer,
primary key (trip_id),
foreign key (driver_id) references drivers(driver_id),
foreign key (bus_id) references bus_info(id));

create table bookings (
booking_id          integer,
trip_id             integer,
traveler_id         integer,
primary key (booking_id),
foreign key (traveler_id) references travelers(id),
foreign key (trip_id) references trip_info(trip_id));


