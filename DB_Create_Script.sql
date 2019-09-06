create table BANKS
(
    BANK_ID int         not null
        primary key,
    NAME    varchar(20) not null
);

create table CARDS
(
    CARD_ID   int         not null
        primary key,
    BANK_ID   int         null,
    NICKNAME  varchar(20) not null,
    NAME      varchar(50) not null,
    LAST_FOUR int         not null,
    constraint CARDS_NICKNAME_uindex
        unique (NICKNAME),
    constraint CARDS_BANKS_BANK_ID_fk
        foreign key (BANK_ID) references BANKS (BANK_ID)
            on update cascade on delete cascade
);

create table EMAILS
(
    EMAIL_ID          int auto_increment
        primary key,
    CARD_ID           int         not null,
    AMOUNT            float       not null,
    MERCHANT_NAME     varchar(50) null,
    MERCHANT_LOCATION varchar(50) null,
    DATE_TIME         datetime    null,
    constraint EMAILS_CARDS_CARD_ID_fk
        foreign key (CARD_ID) references CARDS (CARD_ID)
            on update cascade on delete cascade
);

create table PARSE_BANKS
(
    BANK_ID            int         not null
        primary key,
    IDENTIFIER         varchar(50) not null,
    COMPONENT_ID       int         not null,
    DATE_FORMAT        varchar(30) not null,
    LOCALIZE_DATE_TIME tinyint(1)  not null,
    constraint PARSE_BANKS_IDENTIFIER_uindex
        unique (IDENTIFIER),
    constraint PARSE_BANKS_BANKS_BANK_ID_fk
        foreign key (BANK_ID) references BANKS (BANK_ID)
            on update cascade on delete cascade
);

create table PARSE_COMPONENTS
(
    ID           int auto_increment
        primary key,
    COMPONENT_ID int         not null,
    NAME         varchar(20) null,
    TYPE         varchar(5)  null,
    PREFIX       varchar(50) null,
    POSTFIX      varchar(50) null
);

