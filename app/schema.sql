DROP TABLE IF EXISTS account;
DROP TABLE IF EXISTS video;
DROP TABLE IF EXISTS caption;
DROP TABLE IF EXISTS history;
DROP TABLE IF EXISTS keywords;


create table account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    history_id INTEGER not null,
    code VARCHAR(50) not null
);

create table video (
    video_id INTEGER primary key AUTOINCREMENT,
    url VARCHAR(150) not null,
    file_path VARCHAR(150) not null,
    imagepath VARCHAR(150) not null
);

create table caption(
    caption_id INTEGER primary key AUTOINCREMENT,
    video_id INTEGER references video(video_id) on delete cascade on update cascade,
    start_time int not null,
    end_time int not null,
    content VARCHAR(100) not null,
    count INT not null check(count >= 0)
);

create table history (
    id INTEGER primary key AUTOINCREMENT,
    video_id INTEGER references video(video_id) on delete cascade on update cascade,
    history_id INTEGER references account(history_id) on delete cascade on update cascade
);

create table keywords(
    _id INTEGER primary key AUTOINCREMENT,
    account_id INTEGER references account(history_id) on delete cascade on update cascade,
    caption_id INTEGER references caption(caption_id) on delete cascade on update cascade,
    video_id INTEGER references video(video_id) on delete cascade on update cascade
);
