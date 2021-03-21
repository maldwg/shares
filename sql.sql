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
insert into shares (name, identifier) values ("Atos SE","ATO.PA" );
insert into shares (name, identifier) values ("Beiersdorf","BEI.DE" );
insert into shares (name, identifier) values ("BMW","BMW.DE" );
insert into shares (name, identifier) values ("Deutsche Post","DPW.DE" );   
insert into shares (name, identifier) values ("Siemens","SIE.DE" );
insert into shares (name, identifier) values ("Airbus","AIR.DE" );
insert into shares (name, identifier) values ("Hello Fresh","HFG.DE" );
insert into shares (name, identifier) values ("Siemens Healthineers","SHL.DE" );
insert into shares (name, identifier) values ("Linde plc","LIN.DE" );
insert into shares (name, identifier) values ("Total","TOTB.DE" );
insert into shares (name, identifier) values ("AES","AES.DE" );
insert into shares (name, identifier) values ("Alcoa","185.F" );
insert into shares (name, identifier) values ("AMD","AMD.DE" );
insert into shares (name, identifier) values ("Seagate","STT.MU" );
insert into shares (name, identifier) values ("Kraft-Heinz","KHNZ.DE" );
insert into shares (name, identifier) values ("Nike","NKE.DE" );
insert into shares (name, identifier) values ("Infineon","IFX.DE" );


insert into shares (name, identifier) values ("British American Tobaco","BMT.DE" );
insert into shares (name, identifier) values ("VW","VWAGY" );
insert into shares (name, identifier) values ("Daimler","DAI.DE" );
insert into shares (name, identifier) values ("General Electric","GEC.DE" );
insert into shares (name, identifier) values ("TUI","TUI1.DE" );
insert into shares (name, identifier) values ("Delta Airlines","OYC.DE" );
insert into shares (name, identifier) values ("Deutsche Telekom","DTE.DE" );
insert into shares (name, identifier) values ("Johnson and Johnson","JNJ.DE" );
insert into shares (name, identifier) values ("Biontech","22UA.DE" );
insert into shares (name, identifier) values ("Danone","BSN.F" );
insert into shares (name, identifier) values ("Gartner","GGRA.F" );
insert into shares (name, identifier) values ("Caterpillar","CAT1.F" );
insert into shares (name, identifier) values ("Zalando","ZAL.DE" );
insert into shares (name, identifier) values ("Oracle","ORC.F" );
insert into shares (name, identifier) values ("Lanxess","LXS.DE" );
insert into shares (name, identifier) values ("K + S","SDF.DE" );
insert into shares (name, identifier) values ("Hornbach","HBH.DE" );
insert into shares (name, identifier) values ("Carrefour","CAR.F" );
insert into shares (name, identifier) values ("Kabel Deutschland","KD8.HM" );
insert into shares (name, identifier) values ("Enel","ENL.F" );
insert into shares (name, identifier) values ("JP Morgan","CMC.DE" );
insert into shares (name, identifier) values ("HSBC","HBC1.F" );
insert into shares (name, identifier) values ("RWE","RWE.DE" );
insert into shares (name, identifier) values ("Novartis","NOT.F" );
insert into shares (name, identifier) values ("Sanofi","SNW.F" );
insert into shares (name, identifier) values ("Intel","INL.F" );
insert into shares (name, identifier) values ("AT&T","SOBA.F" );
insert into shares (name, identifier) values ("Telefonica","TNE5.F" );
insert into shares (name, identifier) values ("Prosieben Sat1","PSM.DE" );
insert into shares (name, identifier) values ("Pepsico","PEP.DE" );



insert into portfolio (name, aktuelles_kapital, startkapital) values ("alles", 10000, 10000 );
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,1,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,2,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,3,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,4,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,5,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,6,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,7,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,8,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,9,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,10,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,11,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,12,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,13,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,14,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,15,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,16,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,17,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,18,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,19,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,20,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,21,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,22,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,23,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,24,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,25,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,26,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,27,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,28,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,29,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,30,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,31,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,32,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,33,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,34,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (1,35,0,0);


insert into user (firstname, lastname, mail) values ('Maximilian', 'Ludwig', 'maxludwig23@t-online.de');
insert into portfolio (name, aktuelles_kapital, startkapital) values ('Max Portfolio', '1321.82', '2800');
insert into user_portfolio (portfolio, user) values (2,1);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,1,1,'186.93');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,2,5,'38.66');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,4,2,'76.85');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,6,8,'18.61');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,7,10,'13.08');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,8,40,'2.79');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,9,38,'3.48');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,10,2,'61.31');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,11,0,'0.0');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,12,3,'9.38');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,13,49,'0.600');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,15,4,'60.59');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,21,4,'20.59');
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,3,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,5,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,14,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,16,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,17,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,18,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,19,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,20,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,22,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,23,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,24,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,25,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,26,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,27,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,28,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,29,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,30,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,31,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,32,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,33,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,34,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (2,35,0,0);




insert into portfolio (name, aktuelles_kapital, startkapital) values ("Test-Set", 10000, 10000 );
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,36,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,37,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,38,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,39,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,40,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,41,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,42,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,43,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,44,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,45,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,46,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,47,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,48,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,49,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,50,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,51,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,52,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,53,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,54,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,55,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,56,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,57,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,58,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,59,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,60,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,61,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,62,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,63,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,64,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,65,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,66,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,67,0,0);
insert into portfolio_shares (portfolio, share, anteile, einstandskurs) values (3,68,0,0);
