create table pyq_comment(
	sender_id char(30),
    send_time datetime,
    commenter_id char(30),
    comments text,
    foreign key(sender_id) references users(id)
);

create table pyq_main(
	sender_id char(30),
    send_time datetime,
    content text,
    cool_counter integer,
    primary key(sender_id, send_time),
    foreign key(sender_id) references users(id)
);

create table chat_global(
	sender_id char(30),
    send_time datetime,
    content text,
    foreign key(sender_id) references users(id)
);

create table chat_records(
	sender_id char(30),
    recver_id char(30),
    send_time datetime,
    content text,
    primary key(sender_id, recver_id, send_time),
    foreign key(sender_id) references users(id),
    foreign key(recver_id) references users(id)
);

create table users(
	id char(30),
    pass char(30) not null,
    nick_name char(30) not null,
    primary key(id)
);