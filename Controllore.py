import os
'''
contatore = 0
with open("Controllande.txt", "w", encoding="utf-8") as lavagna:
    for nome in os.listdir("./Grezzi/Tutto"):
        if os.path.getsize(f"./Grezzi/Tutto/{nome}") < 1000:
            contatore += 1
            with open(f"./Grezzi/Tutto/{nome}", "r", encoding="utf-8") as file:
                lavagna.write("OPERA: "+nome+"\nTESTO: ")
                for riga in file:
                    lavagna.write(riga)
                print("\n")
print(contatore)

with open("Controllande.txt", "r", encoding="utf-8") as controllande, open("Controllate.txt", "w", encoding="utf-8") as controllate:
    lista = []
    for riga in controllande:
        if "OPERA:" in riga:
            risposta = input("Premi c per cancellare: ")
            if risposta != "c":
                for elemento in lista:
                    controllate.write(elemento+"\n")
            lista.clear()
        lista.append(riga)
        print(riga)
'''
contatore = 0
with open("Controllate.txt", "r", encoding="utf-8") as file:
    for riga in file:
        if "TESTO:" in riga:
            contatore += 1
print(contatore)
