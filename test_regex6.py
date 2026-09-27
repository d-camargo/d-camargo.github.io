import re
import glob

rx = re.compile(r"\b(não (é |se trata de )?(apenas|somente|só|sobre)|not (just|only|about))\b", re.I)

matches = []
for f in sorted(glob.glob('_posts/*.md')):
    text = open(f).read()
    for m in rx.finditer(text):
        if not f.startswith('_posts/2026-09-27'):
             matches.append(f)
             print(f, m.group(0))
print("Total matches (excluding today):", len(matches))
