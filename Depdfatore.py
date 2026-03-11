import pdfplumber

text = []

with pdfplumber.open("C:\\Users\\aless\\PycharmProjects\\Locutor\\Grezzi\\Tutto\\operaomniaiussui10thom.pdf") as pdf:
    for p, page in enumerate(pdf.pages):
        print(p)
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

with pdfplumber.open("C:\\Users\\aless\\PycharmProjects\\Locutor\\Grezzi\\Tutto\\operaomniaiussui11thom.pdf") as pdf:
    for p, page in enumerate(pdf.pages):
        print(p)
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

with pdfplumber.open("C:\\Users\\aless\\PycharmProjects\\Locutor\\Grezzi\\Tutto\\operaomniaiussui12thom.pdf") as pdf:
    for p, page in enumerate(pdf.pages):
        print(p)
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

full_text = "\n\n".join(text)

with open("C:\\Users\\aless\\PycharmProjects\\Locutor\\Summa_theologicaThomas Aquinas.txt", "a", encoding="utf-8") as f:
    f.write(full_text)
