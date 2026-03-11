import pickle
import os
import re

percorsi = os.listdir("Puliti/Tutto")
percorsi.remove(".DS_Store")
'''
hapax_legomena = set()
non_hapax_legomena = set()
parole_totali = 0
for p, percorso in enumerate(percorsi):
    print(f"\rHapax legomena: {p}/{len(percorsi)}     ", end="")
    with open(f"Puliti/Tutto/{percorso}", "r", encoding="utf-8") as f_:
        testo = f_.read().split()
    for parola in testo:
        parole_totali += 1
        parola = parola.lower().rstrip(".,:;!?")
        if parola not in hapax_legomena:
            hapax_legomena.add(parola)
        elif parola not in non_hapax_legomena:
            non_hapax_legomena.add(parola)
hapax_legomena = hapax_legomena-non_hapax_legomena
print("Numero di hapax legomena:", len(hapax_legomena), len(non_hapax_legomena), parole_totali)
with open("hapax_legomena.pkl", "xb") as hl:
    pickle.dump(hapax_legomena, hl)
with open("hapax_legomena.pkl", "rb") as hl_:
    hl = pickle.load(hl_)
with open("latinizzando.pkl", "xb") as l:
    pickle.dump("", l)
'''
with open("forme_flesse.pkl", "rb") as f:
    accettabili = pickle.load(f)
with open("latinizzando.pkl", "rb") as f:
    latinizzati = pickle.load(f)
spaziofatto = 0
spaziototale = sum(os.path.getsize(f"Puliti/Tutto/{f}") for f in os.listdir("Puliti/Tutto"))
for p, percorso in enumerate(sorted(percorsi)):
    spaziofatto += os.path.getsize(f"Puliti/Tutto/{percorso}")
    if percorso in latinizzati:
        continue
    print(f"Controllo: {p}/{len(percorsi)}: {percorso}, progresso: {spaziofatto}/{spaziototale}")
    with open(f"Puliti/Tutto/{percorso}", "r", encoding="utf-8") as f_:
        testo = f_.read()
    nuovotesto = ""
    for c, capoverso in enumerate(testo.split(".\n")):
        for fr, frase in enumerate(re.findall(r'[^.:;]+(?:[.:;]\s)?', capoverso)):
            with open("rigaattuale.pkl", "rb") as ra:
                ra_ = pickle.load(ra)
                ca, fra, nuovotesto_ = ra_
            if c < ca or fr < fra:
                nuovotesto = nuovotesto_
                continue
            nuovafrase = frase
            for parola in frase.split():
                if len(parola) > 3 and parola[:4] in {"adua", "adue", "adui", "aduo", "aduu", "Adua", "Adue", "Adui",
                                                      "Aduo", "Aduu"}:
                    parola_ = list(parola)
                    parola_[2] = "v"
                    nuovafrase_ = nuovafrase.split(parola, maxsplit=1)
                    nuovafrase = nuovafrase_[0]+"".join(parola_)+nuovafrase_[1]
            frase = nuovafrase
            for parola in frase.split():
                if (parolina := parola.lower().strip("\'\"()").rstrip(".,:;!?")) not in accettabili:
                    if all(paroletta in accettabili for paroletta in parolina.split(",")):
                        continue
                    print("Sospetto:", parolina)
                    frase_ = nuovafrase.split(parola, maxsplit=1)
                    print(f"{frase_[0]}\033[35m{parola}\033[0m{frase_[1]}")
                    richiesta = input("Riscrivi la riga o solo la parola per cambiarle, premi Invio per salvare la parola:\033[31m (Ricorda lo spazio dopo la punteggiatura)\033[0m\n")
                    if richiesta == "":
                        accettabili.add(parolina)
                        with open("forme_flesse.pkl", "wb") as _f:
                            pickle.dump(accettabili, _f)
                    elif " " not in richiesta:
                        nuovafrase = frase_[0]+richiesta.replace("_", " ")+frase_[1]
                        if richiesta not in accettabili:
                            accettabili.add(richiesta.lower().strip("\'\"()").rstrip(".,:;!?"))
                            with open("forme_flesse.pkl", "wb") as _f:
                                pickle.dump(accettabili, _f)
                    else:
                        nuovafrase = richiesta
                        for _parola in richiesta.split():
                            purificata = _parola.lower().strip("\'\"()").rstrip(".,:;!?")
                            if purificata not in accettabili:
                                accettabili.add(purificata)
                        with open("forme_flesse.pkl", "wb") as _f:
                            pickle.dump(accettabili, _f)
                        break
                    print("\033[33m", nuovafrase, "\033[0m")
            nuovotesto += nuovafrase
            with open("rigaattuale.pkl", "wb") as ra_:
                pickle.dump((c, fr, nuovotesto), ra_)
        nuovotesto += ".\n"
    with open(f"Puliti/Tutto/{percorso}", "w", encoding="utf-8") as _f:
        _f.write(nuovotesto)
    with open("latinizzando.pkl", "wb") as l:
        latinizzati.append(percorso)
        pickle.dump(latinizzati, l)
    with open("rigaattuale.pkl", "wb") as _ra:
        pickle.dump((0, 0, ""), _ra)

# Hai fatto una prima regolarizzazione dell'ortografia. Ora:
# Hai fatto un errore che fa sì che le sostituzioni di J, K, ' e W non siano avvenute tutte
# Parole di una sola lettera diverse da "a", "e", ("o")?
# Ricorda che poi dovresti ridurre tutto alla formattazione minima (maiuscole automatiche, spazi post-punteggiatura et similia).
# Ma anche un'uniformazione delle strutture testuali non sarebbe male.
