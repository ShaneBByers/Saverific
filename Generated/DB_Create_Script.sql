create table BANKS
(
	BANK_ID int not null
		primary key,
	NAME varchar(20) not null
);

create table ACCOUNTS
(
	ACCOUNT_ID int not null
		primary key,
	BANK_ID int null,
	NICKNAME varchar(20) not null,
	NAME varchar(50) not null,
	ACCOUNT_NUMBER int not null,
	BALANCE float not null,
	IS_CREDIT tinyint(1) not null,
	`LIMIT` float null,
	constraint CARDS_NICKNAME_uindex
		unique (NICKNAME),
	constraint CARDS_BANKS_BANK_ID_fk
		foreign key (BANK_ID) references BANKS (BANK_ID)
			on update cascade on delete cascade
);

create table EMAILS
(
	EMAIL_ID int auto_increment
		primary key,
	ACCOUNT_ID int not null,
	DATE_TIME datetime not null,
	EMAIL_TYPE_ID int null,
	constraint EMAILS_ACCOUNTS_ACCOUNT_ID_fk
		foreign key (ACCOUNT_ID) references ACCOUNTS (ACCOUNT_ID)
			on update cascade on delete cascade
);

create table BALANCES
(
	EMAIL_ID int not null
		primary key,
	BALANCE int not null,
	constraint BALANCES_EMAILS_EMAIL_ID_fk
		foreign key (EMAIL_ID) references EMAILS (EMAIL_ID)
			on update cascade on delete cascade
);

create table EMAIL_TYPES
(
	EMAIL_TYPE_ID int not null
		primary key,
	`TABLE` varchar(20) not null,
	IS_EMAIL_HTML tinyint(1) not null
);

create table PARSE_BANKS
(
	PARSE_ID int not null
		primary key,
	IDENTIFIER varchar(100) not null,
	BANK_ID int not null,
	DATE_FORMAT varchar(30) not null,
	LOCALIZE_DATE_TIME tinyint(1) not null,
	EMAIL_TYPE_ID int null,
	constraint PARSE_BANKS_IDENTIFIER_uindex
		unique (IDENTIFIER),
	constraint PARSE_BANKS_BANKS_BANK_ID_fk
		foreign key (BANK_ID) references BANKS (BANK_ID)
			on update cascade on delete cascade,
	constraint PARSE_BANKS_EMAIL_TYPES_EMAIL_TYPE_ID_fk
		foreign key (EMAIL_TYPE_ID) references EMAIL_TYPES (EMAIL_TYPE_ID)
			on update cascade on delete cascade
);

create table PARSE_COMPONENTS
(
	PARSE_ID int not null,
	NAME varchar(20) null,
	TYPE varchar(5) null,
	PREFIX varchar(50) null,
	POSTFIX varchar(50) null,
	constraint PARSE_COMPONENTS_PARSE_BANKS_PARSE_ID_fk
		foreign key (PARSE_ID) references PARSE_BANKS (PARSE_ID)
			on update cascade on delete cascade
);

create table TRANSACTIONS
(
	EMAIL_ID int not null
		primary key,
	AMOUNT float null,
	MERCHANT_NAME varchar(50) null,
	MERCHANT_LOCATION varchar(50) null,
	constraint TRANSACTIONS_EMAILS_EMAIL_ID_fk
		foreign key (EMAIL_ID) references EMAILS (EMAIL_ID)
			on update cascade on delete cascade
);


