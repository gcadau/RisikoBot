import telepot
from telepot.loop import MessageLoop
from datetime import datetime
import time
from pprint import pprint
from random import randrange
import math
import sys
from PIL import Image, ImageDraw, ImageFont
import os

TOKEN="1250725908:AAGRl8P9EG9C7Vu7BcY48deXD_b4SRWZi9Q"

class Territorio:
	def __init__(self, x, y, nome):
		self.x = x
		self.y = y
		self.nome = nome
		self.armate = 0
		self.user = ""

class Colore:
	def __init__(self, nome, c1, c2, c3):
		self.nome = nome
		self.c1 = c1
		self.c2 = c2
		self.c3 = c3

class Giocatore:
	def __init__(self, nome, colore):
		self.nome = nome
		self.colore = colore

def on_chat_message(msg):
	bot.setWebhook("")
	test=msg[u'text']
	ch=msg[u'chat']
	fr=msg[u'from']
	i=ch[u'id']
	global nt
	global attacco
	global difesa
	global d1
	global d2
	global territori
	global c
	global n
	global giocatori
	global giocatoriEstr
	global database
	global mazzo
	global obiettivi
	global mappa
	global mazzoOb
	global mela
	global pera
	global plancia
	global colori
	if nt == 2:
		if test.isdigit():
			n = int(test)
			if n < 4 and n > 0:
				d2 = n;
				difesa=fr[u'username']
				nt = 0;
				bot.sendMessage(i, "Lancio dei dadi di " + attacco + "...");
				dadiA = []
				for j in range(d1):
					a = randrange(6);
					a = a+1;
					dadiA.append(a);
					s=("%s %s%s%s" % ("Dado", j+1, ": ", a))
					bot.sendMessage(i, s);
				bot.sendMessage(i, "Lancio dei dadi di " + difesa + "...");
				dadiD = []
				for j in range(d2):
					a = randrange(6);
					a = a+1;
					dadiD.append(a);
					s=("%s %s%s%s" % ("Dado", j+1, ": ", a))
					bot.sendMessage(i, s);
				dadiA.sort(reverse=True);
				dadiD.sort(reverse=True);
				if d1<=d2:
					min = d1;
				else:
					min = d2;
				vA = 0;
				vD = 0;
				for j in range(min):
					if dadiD[j]>=dadiA[j]:
						vA = vA+1;
					else:
						vD = vD+1;
				s=("%s%s%s%s%s%s%s%s" % (attacco, " perde ", vA, " ", "carro armati, ", difesa, " ne perde ", vD))
				bot.sendMessage(i, s);
			else:
				bot.sendMessage(i, "Puoi tirare da 1 a 3 dadi, genio della lampada!");
		else:
			bot.sendMessage(i, "E' tanto difficile mettere un numero? Cosa sei, Di Maio?");
	if nt == 1:
		if test.isdigit():
			n = int(test)
			if n < 4 and n > 0:
				bot.sendMessage(i, "Difendi con?");
				d1 = n;
				attacco=fr[u'username']
				nt = 2;
			else:
				bot.sendMessage(i, "Puoi tirare da 1 a 3 dadi, genio della lampada!");
		else:
			bot.sendMessage(i, "E' tanto difficile mettere un numero? Cosa sei, Di Maio?");
        if "NUOVO TIRO" == test.upper() or "NT" == test.upper():
		resp = bot.getUpdates();
		bot.sendMessage(i, "Attacchi con?");
		nt = 1;
	if nt == 11:
		c = c+1;
		p = fr[u'username']
		v = test.upper()
		j = Giocatore(None, None)
		for z in colori:
			if z.nome == v:
				j = Giocatore(p, z)
		giocatori.append(j)
		if c>=n:
			nt = 12;
	if nt == 10:
		if test.isdigit():
			nt = 11;
			n = int(test);
			bot.sendMessage(i, "Identificatevi! Scrivete il colore delle vostre armate");
		else:
			bot.sendMessage(i, "E' tanto difficile mettere un numero? Cosa sei, Di Maio?");
	if nt == 12:
		bot.sendMessage(i, "Sto mescolando...");
		carte = list(territori);
		carte.pop(43);
		carte.pop(42);
		cPg = len(carte) / n;
		fl = math.floor(cPg);
		rest = len(carte) - (fl*n);
		o = 0;
		gg = n-1;
		if gg < rest:
			f = fl+1;
		else:
			f = fl;
		giocatoriEstr = list(giocatori)
		gioc = giocatoriEstr.pop(gg);
		bot.sendMessage(i, "Carte di " + gioc.nome + ":");
		output = "";
		while len(carte)>0:
			if(o>=f):
				o = 0;
				gg = gg-1;
				if gg < rest:
					f = fl+1;
				else:
					f = fl;
				gioc = giocatoriEstr.pop(gg);
				bot.sendMessage(i, output);
				output = "";
				bot.sendMessage(i, "Carte di " + gioc.nome + ":");
			o = o+1;
			a = randrange(len(carte));
			estr = carte.pop(a);
			output = output + "\n" + estr;
			#bot.sendMessage(i, estr);
		nt = 0;
		c = 0;
		bot.sendMessage(i, output);
	if "DISTRIBUISCI CARTE" == test.upper() or "DC" == test.upper():
		bot.sendMessage(i, "Quanti siete?");
		mazzo = list(database);
		mazzoOb = list(obiettivi);
		nt = 10;
	if "PESCA" == test.upper() or "P" == test.upper():
			a = randrange(len(mazzo));
			if len(mazzo)>0:
				a = randrange(len(mazzo));
				estr = mazzo.pop(a);
				f = open(estr, 'rb')
				bot.sendPhoto(i, f)
				#bot.sendMessage(i, estr);
	if "PESCA OBIETTIVO" == test.upper() or "PO" == test.upper():
			a = randrange(len(mazzoOb));
			if len(mazzoOb)>0:
				a = randrange(len(mazzoOb));
				estr = mazzoOb.pop(a);
				f = open(estr, 'rb')
				bot.sendPhoto(i, f)
				#bot.sendMessage(i, estr);
	if "NUOVA MAPPA" == test.upper() or "NM" == test.upper():
		f = open(mappa, 'rb')
		bot.sendPhoto(i, f)
	if "MELA" == test.upper():
		bot.sendMessage(i, "Giusto, dopo tutte queste pesche ci sta una mela")
		f = open(mela, 'rb')
		bot.sendPhoto(i, f)
		bot.sendMessage(i, "Dai che poi facciamo la macedonia!")
	if "PERA" == test.upper():
		bot.sendMessage(i, "Giusto, dopo tutte queste pesche ci sta una pera")
		f = open(pera, 'rb')
		bot.sendPhoto(i, f)
		bot.sendMessage(i, "Dai che poi facciamo la macedonia!")
	if "AZZERA" == test.upper() or "A" == test.upper():
		mazzo = list(database);
		mazzoOb = list(obiettivi);
	if "MAPPA" == test.upper() or "M" == test.upper():
		image = Image.open(mappa)
		for t in plancia:
			col = Colore("ARANCIONE", 255, 69, 0)
			for s in giocatori:
				if s.nome == t.user:
					col = s.colore
			draw = ImageDraw.Draw(image)
			draw.text(xy=(t.x,t.y),text=str(t.armate), fill=(col.c1,col.c2,col.c3), font=font_type)
		image.save('file.PNG')
		image = Image.open(mappa)
		image.close()
		f = open('file.PNG', 'rb')
		bot.sendDocument(i, f)
		os.remove('file.PNG')
	if "COLORI ARMATE DISPONIBILI" == test.upper() or "CD" == test.upper():
		out = "Colori disponibili:\n"
		for z in colori:
			out = out + z.nome + "\n"
		out = out + "(Richiedi un nuovo colore tramite il comando \"Richiedi nuovo colore armate\")"
		bot.sendMessage(i, out)
	if "RICHIEDI NUOVO COLORE ARMATE" == test.upper() or "NC" == test.upper():
		bot.sendMessage(i, "La tua richiesta e' stata ricevuta, scrivi di seguito il colore")
	try:
		nomeC = (test.upper().split(" ", 1))[1]
		armateI = (test.upper().split(" ", 1))[0]
		try:
			armateC = int(armateI)
			for t in plancia:
				if t.nome == nomeC:
					t.armate = armateC
					t.user = fr[u'username']
		except ValueError:
			armateC = ""
	except IndexError:
		nomeC = ""

bot = telepot.Bot(TOKEN)

nt = 0
attacco = "str"
difesa = "str"
territori = ["Alaska", "Territori del Nord Ovest", "Groenlandia", "Alberta", "Ontario", "Quebec", "Stati Uniti Occidentali", "Stati Uniti Orientali", "America Centrale", "Venezuela", "Peru'", "Brasile", "Argentina", "Islanda", "Scandinavia", "Gran Bretagna", "Europa Settentrionale", "Europa Occidentale", "Europa Meridionale", "Ucraina", "Africa del Nord", "Egitto", "Congo", "Africa Orientale", "Africa del Sud", "Madagascar", "Urali", "Siberia", "Jacuzia", "Cita", "Kamchatka", "Giappone", "Mongolia", "Afghanistan", "Medio Oriente", "India", "Cina", "Siam", "Indonesia", "Nuova Guinea", "Australia Orientale", "Australia Occidentale", "Jolly 1", "Jolly 2"];
database = ["Carte/IMG_1238.JPG", "Carte/IMG_1242.JPG", "Carte/IMG_1245.JPG", "Carte/IMG_1246.JPG", "Carte/IMG_1247.JPG", "Carte/IMG_1248.JPG", "Carte/IMG_1249.JPG", "Carte/IMG_1250.JPG", "Carte/IMG_1251.JPG", "Carte/IMG_1252.JPG", "Carte/IMG_1253.JPG", "Carte/IMG_1254.JPG", "Carte/IMG_1255.JPG", "Carte/IMG_1256.JPG", "Carte/IMG_1257.JPG", "Carte/IMG_1258.JPG", "Carte/IMG_1259.JPG", "Carte/IMG_1260.JPG", "Carte/IMG_1261.JPG", "Carte/IMG_1262.JPG", "Carte/IMG_1263.JPG", "Carte/IMG_1264.JPG", "Carte/IMG_1265.JPG", "Carte/IMG_1266.JPG", "Carte/IMG_1267.JPG", "Carte/IMG_1268.JPG", "Carte/IMG_1269.JPG", "Carte/IMG_1270.JPG", "Carte/IMG_1271.JPG", "Carte/IMG_1272.JPG", "Carte/IMG_1273.JPG", "Carte/IMG_1274.JPG", "Carte/IMG_1275.JPG", "Carte/IMG_1276.JPG", "Carte/IMG_1277.JPG", "Carte/IMG_1278.JPG", "Carte/IMG_1280.JPG", "Carte/IMG_1280.JPG", "Carte/IMG_1281.JPG", "Carte/IMG_1282.JPG", "Carte/IMG_1283.JPG", "Carte/IMG_1284.JPG", "Carte/IMG_1285.JPG", "Carte/IMG_1286.JPG"];
mappa = "Mappa/Plancia.png";
obiettivi = ["Obiettivi/IMG_6797.JPG", "Obiettivi/IMG_6798.JPG", "Obiettivi/IMG_6799.JPG", "Obiettivi/IMG_6800.JPG", "Obiettivi/IMG_6801.JPG", "Obiettivi/IMG_6802.JPG", "Obiettivi/IMG_6803.JPG", "Obiettivi/IMG_6804.JPG", "Obiettivi/IMG_6805.JPG", "Obiettivi/IMG_6806.JPG", "Obiettivi/IMG_6807.JPG", "Obiettivi/IMG_6808.JPG"];
mela = "Altro/mela.jpg"
pera = "Altro/pera.jpeg"
plancia = []
x = Territorio(642, 750, "ALASKA")
plancia.append(x)
x = Territorio(845, 1190, "ALBERTA")
plancia.append(x)
x = Territorio(820, 641, "TERRITORI DEL NORD OVEST")
plancia.append(x)
x = Territorio(1303, 969, "GROENLANDIA")
plancia.append(x)
x = Territorio(1093, 1159, "ONTARIO")
plancia.append(x)
x = Territorio(1516, 1263, "QUEBEC")
plancia.append(x)
x = Territorio(759, 1432, "STATI UNITI OCCIDENTALI")
plancia.append(x)
x = Territorio(1001, 1568, "STATI UNITI ORIENTALI")
plancia.append(x)
x = Territorio(503, 1879, "AMERICA CENTRALE")
plancia.append(x)
x = Territorio(1017, 2214, "VENEZUELA")
plancia.append(x)
x = Territorio(1173, 2656, "BRASILE")
plancia.append(x)
x = Territorio(434, 2577, "PERU")
plancia.append(x)
x = Territorio(700, 3242, "ARGENTINA")
plancia.append(x)
x = Territorio(2404, 687, "ISLANDA")
plancia.append(x)
x = Territorio(2712, 891, "SCANDINAVIA")
plancia.append(x)
x = Territorio(2252, 1248, "GRAN BRETAGNA")
plancia.append(x)
x = Territorio(2770, 1821, "EUROPA MERIDIONALE")
plancia.append(x)
x = Territorio(1945, 1831, "EUROPA OCCIDENTALE")
plancia.append(x)
x = Territorio(2732, 1387, "EUROPA SETTENTRIONALE")
plancia.append(x)
x = Territorio(3005, 1230, "UCRAINA")
plancia.append(x)
x = Territorio(2113, 2148, "AFRICA DEL NORD")
plancia.append(x)
x = Territorio(2562, 2287, "EGITTO")
plancia.append(x)
x = Territorio(2894, 2785, "AFRICA ORIENTALE")
plancia.append(x)
x = Territorio(2621, 2856, "CONGO")
plancia.append(x)
x = Territorio(2721, 3265, "AFRICA DEL SUD")
plancia.append(x)
x = Territorio(3157, 3110, "MADAGASCAR")
plancia.append(x)
x = Territorio(4835, 3358, "AUSTRALIA ORIENTALE")
plancia.append(x)
x = Territorio(4423, 3167, "AUSTRALIA OCCIDENTALE")
plancia.append(x)
x = Territorio(4644, 2406, "INDONESIA")
plancia.append(x)
x = Territorio(5159, 2734, "NUOVA GUINEA")
plancia.append(x)
x = Territorio(4434, 2067, "SIAM")
plancia.append(x)
x = Territorio(3932, 2184, "INDIA")
plancia.append(x)
x = Territorio(4505, 1577, "CINA")
plancia.append(x)
x = Territorio(4023, 1301, "MONGOLIA")
plancia.append(x)
x = Territorio(3317, 1408, "AFGHANISTAN")
plancia.append(x)
x = Territorio(3310, 1064, "URALI")
plancia.append(x)
x = Territorio(3594, 1090, "SIBERIA")
plancia.append(x)
x = Territorio(3806, 994, "CITA")
plancia.append(x)
x = Territorio(3858, 481, "JACUZIA")
plancia.append(x)
x = Territorio(4280, 901, "KAMCHATKA")
plancia.append(x)
x = Territorio(4735, 915, "GIAPPONE")
plancia.append(x)
x = Territorio(3248, 2180, "MEDIO ORIENTE")
plancia.append(x)
giocatori = [];
colori = [];
x = Colore("NERO", 15, 15, 17)
colori.append(x)
x = Colore("BIANCO", 254, 254, 254)
colori.append(x)
x = Colore("VERDE", 35, 194, 41)
colori.append(x)
x = Colore("BLU", 44, 17, 138)
colori.append(x)
x = Colore("ARANCIONE", 255, 69, 0)
colori.append(x)
x = Colore("ROSSO", 215, 2, 2)
colori.append(x)
x = Colore("GIALLO", 205, 8, 193)
colori.append(x)
c = 0;
n = 0;
font_type = ImageFont.truetype('FreeSansBold.ttf',100)

MessageLoop(bot, {'chat': on_chat_message}).run_as_thread();

while 1:
	time.sleep(10)
