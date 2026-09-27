import re
import glob

rx = re.compile(r"\b(?:não é (?:apenas|somente|só|sobre)|not (?:just|only|about))\b", re.I)

matches = []
for f in sorted(glob.glob('_posts/*.md')):
    text = open(f).read()
    for m in rx.finditer(text):
        matches.append(f)
        print(f, m.group(0))
print("Total matches:", len(matches))
