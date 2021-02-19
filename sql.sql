drop table shares;
drop table portfolio_shares;
drop table portfolio;

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
    FOREIGN key (share) references shares(id),
    foreign key (portfolio) references portfolio(id)
);	

insert into shares (name, identifier) values ("Allianz","ALV.DE" );
insert into shares (name, identifier) values ("Fresenius","fre.de" );
insert into shares (name, identifier) values ("SAP","SAP" );
insert into shares (name, identifier) values ("Verbund AG","VER.VI" );
insert into shares (name, identifier) values ("Protektor Forsikring","PR4.F" );
insert into shares (name, identifier) values ("FuelCell","FEY2.BE" );
insert into shares (name, identifier) values ("Ever Fuel","0HR.BE" );
insert into shares (name, identifier) values ("Newage","NBEV" );
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



insert into portfolio (name, aktuelles_kapital, startkapital) values ("alles", 10000, 10000 );

