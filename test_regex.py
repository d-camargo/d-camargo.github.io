import re
import glob

rx1 = re.compile(r"\bNão é (apenas|somente|só|sobre)\b", re.I)
rx2 = re.compile(r"\b(Não é (apenas|somente|só|sobre)|Não se trata de|Not (just|only|about))\b", re.I)
rx3 = re.compile(r"(não é|não se trata|not just|not only|not about)", re.I)
rx4 = re.compile(r"\b(não é|não foi|não se trata|not just|not only|not about)\b", re.I)

for rx in [rx1, rx2, rx3, rx4]:
    matches = []
    for f in sorted(glob.glob('_posts/*.md')):
        text = open(f).read()
        for m in rx.finditer(text):
            matches.append(f)
    print(rx.pattern, len(set(matches)), len(matches))
