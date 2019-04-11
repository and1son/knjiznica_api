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
	nakladnik int not null
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
	datum_izdavanja varchar(100) not null,
	datum_povratka varchar(100) not null,
	cijena float not null,
	izdavatelj int not null,
	knjiga int not null
);

create table korisnici(
	sifra int not null primary key auto_increment,
	public_id varchar(50) not null unique,
	username varchar(50) not null,
	email varchar(32) not null unique,
	password varchar(100) not null,
	admin boolean default '0'
);

create table users(
	id int not null primary key auto_increment,
	first_name varchar(50) not null,
	last_name varchar(50) not null,
	email varchar(50) not null unique,
	password varchar(1000) not null,
	created varchar(50) not null
);

alter table knjiga ADD FOREIGN KEY (nakladnik) REFERENCES nakladnik(sifra);
alter table izdavanje ADD FOREIGN KEY (izdavatelj) REFERENCES izdavatelj(sifra);
alter table izdavanje ADD FOREIGN KEY (knjiga) REFERENCES knjiga(sifra);

use knjiznica;

delimiter $

create trigger foo before insert on knjiga
	for each row
	begin

	if new.Naslov = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Naslov!';
	end if;

	if new.Zanr = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Zanr!';
	end if;

	if new.Autor = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Autora!';
	end if;

	if new.nakladnik = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Nakladnika!';
	end if;
	end;$
delimiter ;

delimiter $

create trigger foo1 before update on knjiga
	for each row
	begin

	if new.Naslov = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Naslov!';
	end if;

	if new.Zanr = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Zanr!';
	end if;

	if new.Autor = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Autora!';
	end if;

	if new.nakladnik = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Nakladnika!';
	end if;
	end;$
delimiter ;

delimiter $

create trigger foo2 before insert on izdavatelj
	for each row
	begin

	if new.Ime = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Ime!';
	end if;

	if new.Prezime = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Prezime!';
	end if;

	if new.Adresa = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Adresa!';
	end if;

	if new.Mjesto = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Mjesto!';
	end if;

	if new.Postanski_broj = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Mjesto!';
	end if;
	

	end;$
delimiter ;

delimiter $

create trigger foo3 before update on izdavatelj
	for each row
	begin

	if new.Ime = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Ime!';
	end if;

	if new.Prezime = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Prezime!';
	end if;

	if new.Adresa = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Adresa!';
	end if;

	if new.Mjesto = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Mjesto!';
	end if;

	if new.Postanski_broj = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Mjesto!';
	end if;
	end;$
delimiter ;

delimiter $

create trigger foo4 before insert on nakladnik
	for each row
	begin

	if new.Naziv = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Naziv!';
	end if;

	if new.Mjesto = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Mjesto!';
	end if;
	end;$

delimiter ;

delimiter $

create trigger foo5 before update on nakladnik
	for each row
	begin

	if new.Naziv = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Naziv!';
	end if;

	if new.Mjesto = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za Mjesto!';
	end if;
	end;$

delimiter ;

delimiter $
create trigger foo6 before insert on izdavanje
	for each row
	begin
	if new.datum_izdavanja = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za datum_izdavanja!';
	end if;

	if new.datum_povratka = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za datum_povratka!';
	end if;

	if new.cijena = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za cijena!';
	end if;

	if new.izdavatelj = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za izdavatelj!';
	end if;

	if new.knjiga = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za knjiga!';
	end if;
	end;$
delimiter ;

delimiter $
create trigger foo7 before update on izdavanje
	for each row
	begin
	if new.datum_izdavanja = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za datum_izdavanja!';
	end if;

	if new.datum_povratka = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za datum_povratka!';
	end if;

	if new.cijena = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za cijena!';
	end if;

	if new.izdavatelj = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za izdavatelj!';
	end if;

	if new.knjiga = '' then
		signal sqlstate '45000' SET MESSAGE_TEXT = 'Upozorenje: Niste unijeli podatke za knjiga!';
	end if;
	end;$
delimiter ;
















