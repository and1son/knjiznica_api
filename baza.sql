drop database if exists knjiznica;
create database knjiznica character set utf8;

use knjiznica;

create table knjiznica(
	sifra int not null PRIMARY KEY auto_increment,
	Naziv varchar(100) not null,
	Mjesto varchar(200) not null,
	Adresa varchar(200) not null,
	Postanski_broj varchar(200) not null
);

create table knjiga(
	sifra int not null PRIMARY KEY auto_increment,
	Naslov varchar(100) not null,
	Zanr varchar(100) not null,
	Autor varchar(100) not null,
	nakladnik int
);

create table izdavatelj(
	sifra int not null PRIMARY KEY auto_increment,
	Ime varchar(100) not null,
	Prezime varchar(100) not null,
	Adresa varchar(100) not null,
	Mjesto varchar(100) not null,
	Postanski_broj varchar(100) not null
);

create table nakladnik(
	sifra int not null PRIMARY KEY auto_increment,
	Naziv varchar(100) not null,
	Mjesto varchar(100) not null
);

create table izdavanje(
	sifra int not null PRIMARY KEY auto_increment,
	datum_izdavanja date,
	datum_povratka date,
	cijena float,
	izdavatelj int,
	knjiga int
);

create table korisnici(
	sifra int not null primary key auto_increment,
	public_id varchar(50) not null unique,
	username varchar(50) not null,
	email varchar(32) not null unique,
	password varchar(100) not null,
	admin boolean default '0'
);

alter table knjiga ADD FOREIGN KEY (nakladnik) REFERENCES nakladnik(sifra);
alter table izdavanje ADD FOREIGN KEY (izdavatelj) REFERENCES izdavatelj(sifra);
alter table izdavanje ADD FOREIGN KEY (knjiga) REFERENCES knjiga(sifra);