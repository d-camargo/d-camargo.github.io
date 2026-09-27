import re
import glob

rx1 = re.compile(r"\bNão é (apenas|somente|só|sobre)\b", re.I)
rx2 = re.compile(r"\bNot (just|only|about)\b", re.I)
rx3 = re.compile(r"\b(?:Não é|Não se trata de) [^.?!;\n]{2,40}(?:,|:)\s*(?:é|mas|mas sim)\b", re.I)
rx4 = re.compile(r"\bNot [^.?!;\n]{2,40}(?:,|:)\s*(?:but|it is)\b", re.I)

matches = []
for f in sorted(glob.glob('_posts/*.md')):
    if f.startswith('_posts/2026-09-27'):
        text = open(f).read()
        for rx in [rx1, rx2, rx3, rx4]:
            if rx.search(text):
                print("MATCH ON TODAY:", f, rx.search(text).group(0))
    else:
        text = open(f).read()
        for rx in [rx1, rx2, rx3, rx4]:
            for m in rx.finditer(text):
                 matches.append(f)
                 print(f, m.group(0).replace("\n", " "))
print("Total matches (excluding today):", len(matches))
