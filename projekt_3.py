"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Zuzana Burešová
email: zuza.buresova@centrum.cz
discord: zuza_34473
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv

url = sys.argv[1]
hlavicka_cast1 = ["kód obce", "název obce", "voliči v seznamu",
                  "vydané obálky", "platné hlasy"]
def kontrola_vstupu():
    if len(sys.argv) != 3:
        sys.exit(f"""
        Nesprávně jsi zadal vstup. Soubor: {sys.argv[0]} 
        potřebuje 2 povinné argumenty.""")
    elif not sys.argv[1].startswith("https://volby.cz/pls/ps2017nss/"):
        sys.exit("Zadal jsi nesprávný odkaz.")
    elif not sys.argv[2].endswith(".csv"):
        sys.exit(f"Soubor: {sys.argv[2]} neni csv soubor!")
    else:
        print(f"STAHUJI DATA Z VYBRANÉHO URL: {sys.argv[1]}")

def ziskej_odpoved_serveru(url: str) -> requests.models.Response:
    return requests.get(url)

def naparsuj_odpoved_na_tagy(odpoved):
    return BeautifulSoup(odpoved.text, features="html.parser")

def ziskej_sloupce_z_prvni_strany(url: str) -> list:
    odpoved_serveru1 = ziskej_odpoved_serveru(url)
    polivka1 = naparsuj_odpoved_na_tagy(odpoved_serveru1)

    tagy_pro_sloupec1 = polivka1.find_all("td", {"class": "cislo"})
    tagy_pro_sloupec2 = polivka1.find_all("td", {"class": "overflow_name"})
    tagy_odkazy_na_obce = polivka1.find_all("td", {"class": "cislo"})
    tagy_odkazy_na_obce_a = [tag_td.findChild() for tag_td in tagy_odkazy_na_obce]

    sloupec1 = [hodnota.text for hodnota in tagy_pro_sloupec1]
    sloupec2 = [hodnota.text for hodnota in tagy_pro_sloupec2]
    odkazy_na_obce_1cast = "https://volby.cz/pls/ps2017nss/"
    odkazy_na_obce_2cast = [hodnota.get("href") for hodnota in tagy_odkazy_na_obce_a]
    odkazy_na_obce = [odkazy_na_obce_1cast+text for text in odkazy_na_obce_2cast]

    return sloupec1, sloupec2, odkazy_na_obce

def ziskej_sloupce_z_druhe_strany(urls: list) -> list:
    polivka2 = []
    for url in urls:
        polivka = naparsuj_odpoved_na_tagy(ziskej_odpoved_serveru(url))
        polivka2.append(polivka)

    sloupec3 = []
    sloupec4 = []
    sloupec5 = []
    for polivka in polivka2:
        polivka3 = polivka.find_all("td", {"headers": "sa2"})
        sloupec3.append(polivka3[0].text)
        polivka4 = polivka.find_all("td", {"headers": "sa3"})
        sloupec4.append(polivka4[0].text)
        polivka5 = polivka.find_all("td", {"headers": "sa6"})
        sloupec5.append(polivka5[0].text)

    sloupec3 = oprav_necitelne_znaky(sloupec3)
    sloupec4 = oprav_necitelne_znaky(sloupec4)
    sloupec5 = oprav_necitelne_znaky(sloupec5)
    
    return sloupec3, sloupec4, sloupec5

def oprav_necitelne_znaky(data: list) -> list:
    data1 = []
    for udaj in data:
        data1.append(udaj.replace("\xa0", ""))
    return data1

def ziskej_seznam_kandidujicich_stran(url:str) -> list:
    # použijeme pro dokončení hlavičky
    odpoved_serveru = ziskej_odpoved_serveru(url)
    polivka = naparsuj_odpoved_na_tagy(odpoved_serveru)
    tagy_strany = polivka.find_all("td", {"class": "overflow_name"})
    nazvy_stran = [hodnota.text for hodnota in tagy_strany]
    return nazvy_stran

def ziskej_volebni_hlasy_pro_1obec(polivka) -> list:
    odstavec_div = polivka.find_all("div", {"id":"inner"})
    odstavec_tr = odstavec_div[0].find_all("tr")
    hlasy = []
    for tr in odstavec_tr:
    # vyhledávání jsem rozdělila na 2 části, protože vstupní data se nacházejí
    # pro každou obec vždy ve 2 tabulkách
        cislo_1cast = tr.find_all("td", {"class":"cislo", "headers":"t1sa2 t1sb3"})
        for td in cislo_1cast:
            hlasy.append(td.text)
        cislo_2cast = tr.find_all("td", {"class":"cislo", "headers":"t2sa2 t2sb3"})
        for td in cislo_2cast:
            hlasy.append(td.text)
    return hlasy

def ziskej_vsechny_volebni_hlasy(urls: str) -> list:
    polivka3 = []
    for url in urls:
        polivka = naparsuj_odpoved_na_tagy(ziskej_odpoved_serveru(url))
        polivka3.append(polivka)
    vsechny_hlasy = []
    for polivka in polivka3:
        hlasy_1obec = ziskej_volebni_hlasy_pro_1obec(polivka)
        vsechny_hlasy.append(hlasy_1obec)
    return vsechny_hlasy

def vytvor_hlavicku(url: str) -> list:
    hlavicka_cast2 = ziskej_seznam_kandidujicich_stran(url)
    hlavicka = hlavicka_cast1 + hlavicka_cast2
    return hlavicka

def priprav_prvni_sloupce_pro_csv(*sloupce: list) -> list:
    seznam_radku = []
    for cislo_radku in range(len(sloupce[0])):
        radek = []
        for sloupec in sloupce:
            radek.append(sloupec[cislo_radku])
        seznam_radku.append(radek)
    return seznam_radku

def priprav_data_pro_csv(data1: list, data2: list) -> list:
    data_pro_csv = []
    for cislo_radku in range(len(data1)):
        radek = []
        radek = data1[cislo_radku] + data2[cislo_radku]
        data_pro_csv.append(radek)
    return data_pro_csv

def nahraj_data_do_csv(hlavicka: list, data: list):
    with open(sys.argv[2], mode="w", newline="", encoding="utf-8") as nove_csv:
        zapisovac = csv.writer(nove_csv)
        zapisovac.writerow(hlavicka)
        zapisovac.writerows(data)
    print(f"UKLADAM DATA DO SOUBORU: {sys.argv[2]}")


def main(url: str):
    sloupce_z_prvni_strany = ziskej_sloupce_z_prvni_strany(url)
    sloupec1, sloupec2 = sloupce_z_prvni_strany[0], sloupce_z_prvni_strany[1]
    odkazy_na_obce = sloupce_z_prvni_strany[2]

    sloupce_z_druhe_strany = ziskej_sloupce_z_druhe_strany(odkazy_na_obce)
    sloupec3 = sloupce_z_druhe_strany[0]
    sloupec4 = sloupce_z_druhe_strany[1]
    sloupec5 = sloupce_z_druhe_strany[2]
    
    hlavicka = vytvor_hlavicku(odkazy_na_obce[0])
    vsechny_hlasy_vsechny_obce = ziskej_vsechny_volebni_hlasy(odkazy_na_obce)
    data_csv_prvni_sloupce = priprav_prvni_sloupce_pro_csv(sloupec1, 
                            sloupec2, sloupec3, sloupec4, sloupec5)
    data_pro_csv = priprav_data_pro_csv(data_csv_prvni_sloupce, vsechny_hlasy_vsechny_obce)
    nahraj_data_do_csv(hlavicka, data_pro_csv)

if __name__ == "__main__":
    kontrola_vstupu()
    main(sys.argv[1])
    print(f"UKONCUJI {sys.argv[0]}")