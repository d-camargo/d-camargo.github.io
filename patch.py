import re

with open("bin/check-content.py", "r") as f:
    lines = f.readlines()

new_lines = []
in_tells = False
for i, line in enumerate(lines):
    if line.startswith("TELLS = ["):
        in_tells = True
        new_lines.append(line)
    elif in_tells and "Não é (apenas|somente|só|sobre)" in line:
        pass # skip this line
    elif in_tells and "estrutura binaria" in line:
        pass # skip this line
    elif in_tells and "]" in line:
        in_tells = False
        new_lines.append(line)
        # insert BINARIOS
        new_lines.append("\n")
        new_lines.append("CORTE_BINARIO = \"2026-09-27\"\n")
        new_lines.append("BINARIOS = [\n")
        new_lines.append("    (re.compile(r\"\\bNão é (apenas|somente|só|sobre)\\b\", re.I),\n")
        new_lines.append("     \"estrutura binaria 'Não é apenas/sobre X' (proibida)\"),\n")
        new_lines.append("    (re.compile(r\"\\b(not (just|only|about))\\b\", re.I),\n")
        new_lines.append("     \"estrutura binaria 'not just/about X' (proibida)\"),\n")
        new_lines.append("]\n")
        new_lines.append("\n")
        new_lines.append("CASOS_BINARIO = [\n")
        new_lines.append("    (\"Não é apenas sobre código\", True),\n")
        new_lines.append("    (\"não é só isso\", True),\n")
        new_lines.append("    (\"Isso não é verdade\", False),\n")
        new_lines.append("    (\"not just code\", True),\n")
        new_lines.append("    (\"not only that\", True),\n")
        new_lines.append("    (\"not exactly\", False),\n")
        new_lines.append("]\n")
        new_lines.append("\n")
        new_lines.append("for caso, esperado in CASOS_BINARIO:\n")
        new_lines.append("    bateu = any(rx.search(caso) for rx, _ in BINARIOS)\n")
        new_lines.append("    if bateu != esperado:\n")
        new_lines.append("        raise RuntimeError(f\"Erro no autoteste BINARIOS: '{caso}' classificou como {bateu}\")\n")
        new_lines.append("\n")
    else:
        new_lines.append(line)

with open("bin/check-content.py", "w") as f:
    f.writelines(new_lines)

