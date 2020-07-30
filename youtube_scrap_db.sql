create table youtube_Influencer(
   username varchar(50),
    scrap_time datetime,
    followers int
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
alter table youtube_Influencer add primary key(username, scrap_time);


create table youtube_post(
    id varchar(500),
    scrap_time datetime,
    title varchar(2000),
    post_time varchar(50),
    username varchar(50),
    likes varchar(50),
    comments int

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
alter table youtube_post add primary key(id, scrap_time);
