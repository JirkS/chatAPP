CREATE TABLE users(
id int primary key AUTO_INCREMENT,
name varchar(20) not null,
email varchar(50) not null,
password varchar(255) not null
);

CREATE TABLE message(
id int primary key AUTO_INCREMENT,
SenderID int not null,
MessageText varchar(255) not null,
RoomID int not null,
Timestamp timestamp default CURRENT_TIMESTAMP,
foreign key (SenderID) references users(id),
);