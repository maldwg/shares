drop table portfolio_shares;
drop table user_portfolio;
drop table portfolio;
drop table user;
drop table shares;

create table shares(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    name varchar(30),
    identifier varchar(30)
);

create table portfolio(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    name varchar(30),
    aktuelles_kapital FLOAT,
    startkapital FLOAT
);

create table portfolio_shares(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio int,
    share int,
    anteile int,
    einstandskurs float,
    UNIQUE(portfolio,share),
    FOREIGN key (share) references shares(id),
    foreign key (portfolio) references portfolio(id)
);	

create Table 'user'(
id  INTEGER PRIMARY KEY AUTOINCREMENT,
firstname varchar(15),
lastname varchar(15),
mail varchar(50),
UNIQUE(firstname, lastname)
);

create Table 'user_portfolio'(
id  INTEGER PRIMARY KEY AUTOINCREMENT,
portfolio INTEGER,
user INTEGER,
FOREIGN KEY (portfolio) references portfolio(id),
FOREIGN KEY (user) references user(id)
);

insert into shares (name, identifier) values ("Allianz","ALV.DE" );
insert into shares (name, identifier) values ("Fresenius","fre.de" );
insert into shares (name, identifier) values ("SAP","SAP" );
insert into shares (name, identifier) values ("Verbund AG","VER.VI" );
insert into shares (name, identifier) values ("Protektor Forsikring","PR4.F" );
insert into shares (name, identifier) values ("FuelCell","FEY2.BE" );
insert into shares (name, identifier) values ("Ever Fuel","0HR.BE" );
insert into shares (name, identifier) values ("Newage","N1K.BE" );
insert into shares (name, identifier) values ("Xiamoi","3CP.F" );
insert into shares (name, identifier) values ("Plugpower","PLUN.BE" );
insert into shares (name, identifier) values ("AXA","CS.PA" );
insert into shares (name, identifier) values ("EON","EON.BR" );
insert into shares (name, identifier) values ("AMP","C4T.BE" );
insert into shares (name, identifier) values ("BAYER","BAYN.DE" );
insert into shares (name, identifier) values ("BASF","BAS.DE" );
insert into shares (name, identifier) values ("MSFT","MSFT" );
insert into shares (name, identifier) values ("Lufthansa","LHA.DE" );
insert into shares (name, identifier) values ("Thyssen Krupp","TKA.DE" );
insert into shares (name, identifier) values ("SANTANDER","SAN" );
insert into shares (name, identifier) values ("BP","BP" );
insert into shares (name, identifier) values ("Volvo","VOL1.F" );



insert into portfolio (name, aktuelles_kapital, startkapital) values ("alles", 10000, 10000 );
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,1,10,200);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,2,5,100);


insert into user (firstname, lastname, mail) values ('Maximilian', 'Ludwig', 'maxludwig23@t-online.de');
insert into portfolio (name, aktuelles_kapital, startkapital) values ('Max Portfolio', '977,23', '2500');
insert into user_portfolio (portfolio, user) values (2,1);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,1,1,'186.93');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,2,5,'38.66');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,4,2,'76.85');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,6,8,'18.61');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,7,10,'13.08');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,8,40,'2.79');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,9,38,'3.48');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,10,2,'61.31');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,11,2,'20.20');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,12,3,'9.38');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,13,49,'0.600');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,15,4,'60.59');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,21,4,'20.59');





