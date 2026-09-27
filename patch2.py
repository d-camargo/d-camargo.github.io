with open("bin/check-content.py", "r") as f:
    text = f.read()

check_code = """
        # --- marcas de texto gerado ---
        for rx, msg in TELLS:
            for m in rx.finditer(corpo):
                linha = off + corpo[: m.start()].count("\\n")
                trecho = corpo[max(0, m.start() - 30): m.start() + 40].replace("\\n", " ").strip()
                err(linha, f"{msg} → ...{trecho}...")

        # --- regra binarios ---
        data_post = f.name[:10]
        for rx, msg in BINARIOS:
            for m in rx.finditer(corpo):
                linha = off + corpo[: m.start()].count("\\n")
                trecho = corpo[max(0, m.start() - 30): m.start() + 40].replace("\\n", " ").strip()
                if data_post >= CORTE_BINARIO:
                    err(linha, f"{msg} → ...{trecho}...")
                else:
                    avisos.append((rel, linha, f"{msg} → ...{trecho}..."))
"""
text = text.replace("""
        # --- marcas de texto gerado ---
        for rx, msg in TELLS:
            for m in rx.finditer(corpo):
                linha = off + corpo[: m.start()].count("\\n")
                trecho = corpo[max(0, m.start() - 30): m.start() + 40].replace("\\n", " ").strip()
                err(linha, f"{msg} → ...{trecho}...")""", check_code)

with open("bin/check-content.py", "w") as f:
    f.write(text)

