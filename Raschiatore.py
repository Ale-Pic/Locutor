import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from os.path import getsize, exists
from os import remove
import lxml

_API = "https://la.wikisource.org/w/api.php"


def raschiasecoli():
    parametri = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": "Categoria:Scriptorum_index_chronologicus",
        "cmlimit": "max",
        "cmtype": "page|subcat",
        "format": "json"
    }
    secoli = []
    while True:
        time.sleep(1.1)
        r = requests.get(_API, params=parametri, headers={
        "User-Agent": "Toadino2 (contact: alessandro.piccirilli.2000@gmail.com)"})
        print(r.status_code)
        print(r.headers)
        print(repr(r.text))
        r.raise_for_status()
        r = r.json()
        for lemma in r["query"]["categorymembers"]:
            secoli.append(lemma["title"].split(":")[-1])
        if "continue" in r:
            parametri.update(r["continue"])
        else:
            break
    return secoli


def raschiaautori(secolo):
    parametri = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Categoria:{secolo}",
        "cmlimit": "max",
        "cmtype": "page|subcat",
        "format": "json"
    }
    autori = list()
    while True:
        time.sleep(1.1)
        r = requests.get(_API, params=parametri, headers={
        "User-Agent": "Toadino2 (contact: alessandro.piccirilli.2000@gmail.com)"})
        r.raise_for_status()
        r = r.json()
        if "query" not in r:
            print("Eh?", repr(r))
        for lemma in r["query"]["categorymembers"]:
            autori.append(lemma["title"].split(":")[-1])
        if "continue" in r:
            parametri.update(r["continue"])
        else:
            break
    return autori


def raschiaincerti():
    parametri = {"action": "query", "list": "categorymembers", "cmtitle": f"Categoria:Opera_quae_Auctor_incertus_scripsit",
                 "cmlimit": "max", "cmtype": "page|subcat", "format": "json"}
    opere = list()
    while True:
        time.sleep(1.1)
        r = requests.get(_API, params=parametri, headers={"User-Agent":
                                                              "Toadino2 (contact: alessandro.piccirilli.2000@gmail.com)"})
        r.raise_for_status()
        r = r.json()
        for lemma in r["query"]["categorymembers"]:
            opere.append(lemma["title"])
        if "continue" in r:
            parametri.update(r["continue"])
        else:
            break
    return opere


def raschiavari():
    parametri = {"action": "query", "list": "categorymembers", "cmtitle": f"Categoria:Opera_quae_Auctores_varii_scripsit",
                 "cmlimit": "max", "cmtype": "page|subcat", "format": "json"}
    opere = list()
    while True:
        time.sleep(1.1)
        r = requests.get(_API, params=parametri, headers={
                 "User-Agent": "Toadino2 (contact: alessandro.piccirilli.2000@gmail.com)"})
        r.raise_for_status()
        r = r.json()
        for lemma in r["query"]["categorymembers"]:
            opere.append(lemma["title"])
        if "continue" in r:
            parametri.update(r["continue"])
        else:
            break
    return opere


def zuppatore(link):
    try:
        print(f"Richiedo {link}")
        time.sleep(1.1)
        r = requests.get(link, headers={"User-Agent": "Toadino2 (contact: alessandro.piccirilli.2000@gmail.com)"})
        r.raise_for_status()
        return BeautifulSoup(r.text, "lxml")
    except requests.exceptions.HTTPError:
        print(f"Questa pagina non esisteva")
        return None


def raschiaopere(linkautore):
    zuppa = zuppatore(linkautore)
    if zuppa is None:
        return None
    opere = list()
    contenuto = zuppa.find("div", class_="mw-content-container")
    for a in contenuto.find_all("a", href=True):
        iperriferimento = a["href"]
        if "class" in a.attrs and "new" in a["class"]:
            continue
        pagina = iperriferimento.split("/wiki/")[-1]
        if ":" in pagina or not iperriferimento.startswith("/wiki"):
            continue
        opere.append(urljoin("https://la.wikisource.org", iperriferimento))
    return list(set(opere))


def raschiatesto(zuppa):
    contenuto = zuppa.find("div", class_="mw-content-container")
    paragrafi = contenuto.find_all("p")
    testo = "\n\n".join(paragrafo.get_text(strip=True) for paragrafo in paragrafi)
    print("Testo trovato:", testo[:100])
    return testo.strip()


def èindice(zuppa, titolo):
    contenuto = zuppa.find("div", class_="mw-content-container")
    if not contenuto:
        return False
    figli = 0
    for a in contenuto.find_all("a", href=True):
        href = a["href"]
        if not href.startswith("/wiki/"):
            continue
        nome = titolo.split("/")[-1]
        pagina = href.split("/wiki/")[-1]
        #print(pagina, nome, pagina.startswith(nome+"_("))
        if pagina.startswith(nome + "/") or pagina.startswith(nome + "_("):
            figli += 1
            if figli >= 2:
                return True
    return False


def raschia(titolo, livello: int):
    if livello > 5:
        print("Ricorsione massima raggiunta")
        return ""
    else:
        print("Livello di ricorsione:", livello)
        livello += 1
    raschiume = ""
    sovrapagina = f"https://la.wikisource.org/wiki/{titolo}"
    zuppa = zuppatore(sovrapagina)
    if zuppa is None:
        return "zyxwvu"
    if not èindice(zuppa, sovrapagina):
        raschiume += raschiatesto(zuppa)+"\n"
        print("Ho raschiato:", raschiume[:100] if len(raschiume) > 100 else raschiume)
    else:
        contenuto = zuppa.find("div", class_="mw-content-container")
        libri = list()
        for a in contenuto.find_all("a", href=True):
            iperriferimento = a["href"]
            #print("Trovato iperriferimento raschiando:", iperriferimento)
            if "class" in a.attrs and "new" in a["class"]:
                continue
            sito = iperriferimento.split("/")
            pagina = iperriferimento.split("/wiki/")[-1]
            #print("Sito:", sito)
            #print("Pagina:", pagina)
            if ":" in pagina or "wiki" not in sito or titolo not in pagina or titolo == pagina:
                continue
            libri.append(pagina)
        print("Libri:", libri)
        for libro in libri:
            raschiume += raschia(libro, livello)
    return raschiume


def epoca(secolo):
    if "vicesimi" in secolo or "septimi decimi" in secolo:
        return "Moderno"
    elif "quarti decimi" in secolo or "quinti decimi" in secolo or "sexti decimi" in secolo:
        return "Rinascimentale"
    elif "ante" in secolo or "primi" in secolo or "secundi" in secolo or "a.Ch.n." in secolo:
        return "Classico"
    elif "septimi" in secolo or "octavi" in secolo or "noni" in secolo or "decimi" in secolo or "undecimi" in secolo or "duodecimi" in secolo or "tertii decimi" in secolo:
        return "Medievale"
    elif "tertii" in secolo or "quarti" in secolo or "quinti" in secolo or "sexti" in secolo:
        return "Tardo"
    else:
        return "Moderno"


def genitivo(autore):
    componenti = autore.split(" ")
    nuovonome = list()
    for componente in componenti:
        caratteri = list(componente)
        if caratteri[-1] == "a":
            caratteri[-1] = "ae"
        elif caratteri[-2:] == ["u", "s"]:
            caratteri[-2] = "i"
            caratteri[-1] = ""
        elif caratteri[-2:] == ["a", "r"]:
            caratteri[-2] = "aris"
            caratteri[-1] = ""
        elif caratteri[-1] == "o":
            caratteri[-1] = "onis"
        elif caratteri[-2:] == ["a", "l"]:
            caratteri[-2] = "alis"
            caratteri[-1] = ""
        elif caratteri[-2:] == ["o", "r"]:
            caratteri[-2] = "oris"
            caratteri[-1] = ""
        elif len(caratteri) > 4 and caratteri[-4:] == ["o", "r", "e", "s"]:
            caratteri[-4] = "orum"
            caratteri[-3] = ""
            caratteri[-2] = ""
            caratteri[-1] = ""
        elif caratteri[-1] == "i":
            caratteri[-1] = "orum"
        elif caratteri[-2:] == ["e", "s"]:
            caratteri[-2] = "is"
            caratteri[-1] = ""
        elif componente == "Nepos":
            nuovonome.append("Nepotis")
        nuovonome.append("".join(caratteri))
    return " ".join(nuovonome)


def denominazione(titolo: str, autore):
    return "".join(parola.capitalize() for parola in titolo.split(" "))+genitivo(autore)


def salva(secolo, autore, titolo, testo):
    percorso = f"./Grezzi/{epoca(secolo)}/{denominazione(titolo, autore)}.txt"
    try:
        with open(percorso, "x", encoding="utf-8") as file:
            file.write(testo)
    except FileExistsError:
        print(f"Il file esisteva già: {percorso}")
    except Exception as e:
        print("Errore inaspettato:", e)
    else:
        print(f"Ho salvato {percorso} con {getsize(percorso)} byte")
        if getsize(percorso) < 2:
            print("FILE VUOTO")
    try:
        with open(f"./Grezzi/Tutto/{denominazione(titolo, autore)}.txt", "x", encoding="utf-8") as file:
            file.write(testo)
    except FileExistsError:
        print(f"Il file esisteva già: ./Grezzi/Tutto/{denominazione(titolo, autore)}.txt")
    except Exception as e:
        print("Errore inaspettato:", e)


numeri = [(" xxi", "primi vicesimi"), (" xx", "vicesimi"), (" xix", "undevicesimi"), (" xviii", "duodevicesimi"),
          (" xvii", "septimi decimi"), (" xvi", "sexti decimi"), (" xv", "quinti decimi"), (" xiv", "quarti decimi"),
          (" xiii", "tertii decimi"), (" xii", "duodecimi"), (" xi", "undecimi"), (" x", "decimi"),
          (" ix", "noni"), (" viii", "octavi"), (" vii", "septimi"), (" vi", "sexti"), (" v", "quinti"),
          (" iv", "quarti"), (" iii", "tertii"), (" ii", "secundi"), (" i", "primi")]


def paginaintera(opera):
    zuppa = zuppatore(f"https://la.wikisource.org/wiki/{opera}")
    if zuppa is None:
        return "Vuota", "Ignotum"
    contenuto = zuppa.find("div", class_="titulusHeaderBox")
    testo = raschia(opera, 0)
    if not contenuto:
        return testo, "Ignotum"
    for div in contenuto.find_all("div"):
        stringa = div.get_text(strip=True).lower()
        if "saeculo" in stringa:
            for numero in numeri:
                if numero[0] in stringa:
                    stringa += numero[1]
                    return testo, stringa
            return testo, "Ignotum"
    return testo, "Ignotum"


import pickle


def raschiatore():
    if exists("Raschiatura.pkl"):
        with open("Raschiatura.pkl", "rb") as file:
            opere = pickle.load(file)
        print("Ho recuperato le opere")
    else:
        secoli = raschiasecoli()
        if "Saeculi incogniti scriptores" in secoli:
            secoli.remove("Saeculi incogniti scriptores")
        if "Saeculi noni ante Christum scriptores" in secoli:
            secoli.remove("Saeculi noni ante Christum scriptores")
        print(secoli)
        autori = dict()
        for secolo in secoli:
            autori[secolo] = raschiaautori(secolo)
        opere = dict()
        for secolo in autori:
            opere[secolo] = dict()
            for autore in autori[secolo]:
                opere[secolo][autore.split(":")[-1]] = raschiaopere(f"https://la.wikisource.org/wiki/Scriptor:{autore}")
        with open("Raschiatura.pkl", "xb") as file:
            pickle.dump(opere, file)
    controllande = list()
    for secolo in opere:
        for autore in opere[secolo]:
            for opera in opere[secolo][autore]:
                titolo = opera.split("/wiki/")[-1]
                if not exists(f"./Grezzi/Tutto/{denominazione(titolo, autore)}.txt"):
                    testo = raschia(titolo, 0)
                    salva(secolo, autore, titolo, testo)
                elif getsize(f"./Grezzi/Tutto/{denominazione(titolo, autore)}.txt") < 500:
                    rimozione = False
                    with open(f"./Grezzi/Tutto/{denominazione(titolo, autore)}.txt", "r", encoding="utf-8") as testovecchio:
                        if (all((all(carattere in {" ", "\n"} for carattere in riga)) for riga in testovecchio) or
                                any(("index" in riga or "INDEX" in riga or "Index" in riga) for riga in testovecchio)):
                            rimozione = True
                    if rimozione:
                        remove(f"./Grezzi/Tutto/{denominazione(titolo, autore)}.txt")
                        testo = raschia(titolo, 0)
                        if len(testo) < 500:
                            print(f"Ahia: {opera}")
                            controllande.append(opera)
                        if testo != "zyxwvu":
                            salva(secolo, autore, titolo, testo)
                else:
                    print("Il file esisteva già: ", denominazione(titolo, autore))
    opereincerte = raschiaincerti()
    for opera in opereincerte:
        if not exists(f"./Grezzi/Tutto/{opera}Auctoris incerti.txt"):
            testo, secolo = paginaintera(opera)
            if len(testo) < 500:
                print(f"Ahia: {opera}")
                controllande.append((testo, secolo))
            if testo != "Vuota":
                salva(secolo, "Auctor incertus", opera, testo)
        elif getsize(f"./Grezzi/Tutto/{opera}Auctoris incerti.txt") < 500:
            rimozione = False
            with open(f"./Grezzi/Tutto/{opera}Auctoris incerti.txt", "r") as testovecchio:
                if (all((all(carattere in {" ", "\n"} for carattere in
                             riga) or "index" in riga or "INDEX" in riga or "Index" in riga) for riga in testovecchio)):
                    rimozione = True
            if rimozione:
                remove(f"./Grezzi/Tutto/{opera}Auctoris incerti.txt")
                testo, secolo = paginaintera(opera)
                if len(testo) < 500:
                    print(f"Ahia: {opera}")
                    controllande.append((testo, secolo))
                if testo != "Vuota":
                    salva(secolo, "Auctor incertus", opera, testo)
    operevarie = raschiavari()
    for opera in operevarie:
        if not exists(f"./Grezzi/Tutto/{opera}Auctorum variorum.txt"):
            testo, secolo = paginaintera(opera)
            if len(testo) < 500:
                print(f"Ahia: {opera}")
                controllande.append((testo, secolo))
            if testo != "Vuota":
                salva(secolo, "Auctores varii", opera, testo)
        elif getsize(f"./Grezzi/Tutto/{opera}Auctorum variorum.txt") < 500:
            rimozione = False
            with open(f"./Grezzi/Tutto/{opera}Auctorum variorum.txt", "r") as testovecchio:
                if (all((all(carattere in {" ", "\n"} for carattere in
                             riga) or "index" in riga or "INDEX" in riga or "Index" in riga) for riga in testovecchio)):
                    rimozione = True
            if rimozione:
                remove(f"./Grezzi/Tutto/{opera}Auctorum variorum.txt")
                testo, secolo = paginaintera(opera)
                if len(testo) < 500:
                    print(f"Ahia: {opera}")
                    controllande.append((testo, secolo))
                if testo != "Vuota":
                    salva(secolo, "Auctores varii", opera, testo)
    print(controllande)


if __name__ == "__main__":
    cronometro = time.time()
    raschiatore()
    secondi = time.time()-cronometro
    print(f"\033[35mHo finito in {secondi} secondi")

# Hai ancora alcuni file sospettosamente corti
# Alcuni file si trovano solo nella cartella Tutto
