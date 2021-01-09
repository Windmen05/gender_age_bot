create table if not exists users
(
    chat_id   bigint            not null
        constraint users_pk
            primary key,
    username  text,
    full_name text,
    id        serial            not null
);

create table if not exists user_preds
(
    chat_id          bigint     not null,
    file_unique_id   text,
    pred_chance      smallint,
    pred_sex         boolean,
    pred_age         smallint,
    id               serial     not null
);


alter table users
    owner to postgres;

alter table user_preds
    owner to postgres;


create unique index if not exists users_id_uindex
    on users (id);

create unique index if not exists user_preds_id_uindex
    on user_preds (id);