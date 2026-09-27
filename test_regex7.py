import re
import glob

rx1 = re.compile(r"\b(?:não (?:é|se trata de|foi) (?:apenas|somente|só|sobre)|not (?:just|only|about))\b", re.I)
rx2 = re.compile(r"\b(?:não (?:é|foi)).{1,40}(?:,|:|\.)\s*(?:mas|é|são|foi)\b", re.I)
rx3 = re.compile(r"(?i)\bnão (é|foi|se trata)\b[^\.\:]{0,40}?(\:|, mas)\b")

for f in sorted(glob.glob('_posts/*.md')):
    if f.startswith('_posts/2026-09-27'): continue
    text = open(f).read()
    for m in rx2.finditer(text):
        print(f, m.group(0).replace("\n", " "))
