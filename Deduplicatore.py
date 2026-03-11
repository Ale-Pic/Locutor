import os
import pickle
import re
import hashlib
from collections import defaultdict
from itertools import combinations
import time
import multiprocessing as mp


def normalizza(testo: str) -> str:
    testo = testo.lower()
    testo = testo.replace('\n', ' ')
    testo = testo.replace(".", "")
    testo = testo.replace(",", "")
    return testo


def hasha(stringa: str) -> int:
    return int.from_bytes(hashlib.blake2b(stringa.encode("utf-8", errors="ignore"), digest_size=8).digest(), byteorder="little", signed=False)


def simhasha(testo: str) -> tuple[int, int]:
    vettore = [0]*64
    parole = normalizza(testo).split()
    for parola in parole:
        hash = hasha(parola)
        for i in range(64):
            bit = (hash >> i) & 1
            vettore[i] += 1 if bit else -1
    firma = 0
    for indice, punteggio in enumerate(vettore):
        if punteggio > 0:
            firma |= (1 << indice)
    return firma, firma.bit_count()


def distanza_di_hamming(a: int, b: int) -> int:
    return (a^b).bit_count()


def leggi(percorso: str) -> str:
    with open(percorso, "rb") as f:
        dati = f.read()
    return dati.decode("utf-8", errors="ignore")


def hash_riga_esatta(riga: str) -> bytes:
    # 16 byte bastano, collisioni astronomicamente improbabili per uso pratico
    return hashlib.blake2b(riga.encode("utf-8", errors="ignore"), digest_size=16).digest()


def trova_duplicati_esatti(percorsi):
    duplicati = {}
    lpercorsi = len(percorsi)
    for p, percorso in enumerate(percorsi):
        testo = leggi("Puliti/Tutto/" + percorso).split("\n")
        ltesto = len(testo)
        for r, riga in enumerate(testo):
            print("\r", r, "-", p, "/", ltesto, "-", lpercorsi, sep="", end="")
            if riga == "" or len(riga) < 50:
                continue
            nr = normalizza(riga)
            h = hash_riga_esatta(nr)
            if h in duplicati:
                duplicati[h].append((p, r))
            else:
                duplicati[h] = [(p, r)]
    return {hash: duplicati[hash] for hash in duplicati if len(duplicati[hash]) > 1}

'''
if __name__ == "__main__":
    percorsi = os.listdir("Puliti/Tutto")
    percorsi.remove(".DS_Store")
    percorsi = sorted(percorsi)
    duplicatini = trova_duplicati_esatti(percorsi)
    with open("Duplicati.pkl", "xb") as f:
        pickle.dump(duplicatini, f)
    print()
    for duplicato in duplicatini:
        print(duplicato, duplicatini[duplicato])
'''

if __name__ == "__main__":
    percorsi = os.listdir("Puliti/Tutto")
    percorsi.remove(".DS_Store")
    percorsi = sorted(percorsi)
    percorsi = [(percorso, os.path.getsize("Puliti/Tutto/"+percorso)) for percorso in percorsi]
    with open("Duplicati.pkl", "rb") as f:
        duplicati = pickle.load(f)
    opere_duplicate_sospette = dict()
    for duplicato in duplicati.values():
        if len(duplicato) == 2 and duplicato[0][1] == duplicato[1][1]:
            if (duplicato[0][0], duplicato[1][0]) in opere_duplicate_sospette:
                opere_duplicate_sospette[(duplicato[0][0], duplicato[1][0])] += 1
            else:
                opere_duplicate_sospette[(duplicato[0][0], duplicato[1][0])] = 1
    for opera in opere_duplicate_sospette:
        taglia1, taglia2 = percorsi[opera[0]][1], percorsi[opera[1]][1]
        print("-" if taglia1 == taglia2 else "", (opere_duplicate_sospette[opera], percorsi[opera[0]], percorsi[opera[1]]))
    print(len(opere_duplicate_sospette))
