import re
import glob

rx_pt = re.compile(r"\b(não (?:é|se trata de) [^.?!;]{2,50}?(?:,|:|;)\s*(?:é|mas|mas sim)\b|não é (?:apenas|somente|só|sobre)\b)", re.I)
rx_en = re.compile(r"\b(not (?:just|only|about)\b|not [^.?!;]{2,50}?(?:,|:|;)\s*(?:but|it is)\b)", re.I)

matches = []
for f in sorted(glob.glob('_posts/*.md')):
    text = open(f).read()
    for rx in [rx_pt, rx_en]:
        for m in rx.finditer(text):
            if not f.startswith('_posts/2026-09-27'):
                 matches.append(f)
                 print(f, m.group(0).replace("\n", " "))
print("Total matches (excluding today):", len(matches))
