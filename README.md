# engeto-projekt-3
Elections Scraper

Tento projekt slouží k extrahování výsledků z parlamentních voleb v roce 2017.

Instalace knihoven

Použité knihovny jsou uloženy v requirements.txt. Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:

$ pip3 --version  # ověřím verzi manažeru
$ pip3 install -r requirements.txt  # nainstalujeme knihovny

Spuštění projektu

Spuštění souboru projekt_3.py v rámci příkazového řádku požaduje 2 povinné argumenty.

1. <odkaz na volební výsledky zvoleného okresu>
2. <nazev vysledneho csv dokumentu>

Následně se stáhne soubor .csv s výsledky voleb v daném okresu.

Příklad spuštění programu

python projekt_3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5202" "jicin_volby.csv"

Příklad běhu programu:

STAHUJI DATA Z VYBRANÉHO URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5202

UKLADAM DATA DO SOUBORU: jicin_volby.csv

UKONCUJI projekt_3.py

Ukázka z výstupu:

kód obce,název obce,voliči v seznamu,vydané obálky,platné hlasy,Občanská demokratická strana,...
553701,Bačalky,133,98,97,12,0,0,5,0,5,9,1,5,1,0,0,14,0,4,34,0,1,1,0,0,0,5,0
572667,Bašnice,170,116,115,8,0,0,5,0,8,7,0,1,0,0,0,4,0,2,59,0,0,7,2,0,0,12,0
572675,Běchary,230,98,96,4,0,0,10,0,3,3,0,3,1,0,0,7,0,0,42,0,0,6,0,0,0,17,0
...
