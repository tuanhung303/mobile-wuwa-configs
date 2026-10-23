"""Print the cvars each Scalability section sets, from a decrypted Client.log.

Usage: python3 sections.py Client.log.txt
Only the first pass of each section is printed; [locked:X] means a higher
priority (X) kept its value.
"""
import re, sys
cur = None; seen = {}; order = []
for line in open(sys.argv[1], encoding='utf-8', errors='replace'):
    m = re.search(r"Applying CVar settings from Section \[([^\]]+)\] File \[([^\]]+)\]", line)
    if m:
        cur = m.group(1) + ('' if 'Scalability' in m.group(2) else ' <' + m.group(2).split('/')[-1] + '>')
        if cur in seen: cur = None; continue
        seen[cur] = []; order.append(cur); continue
    if cur is None: continue
    m = re.search(r"Setting CVar \[\[([^:\]]+):([^\]]*)\]\]", line)
    if m: seen[cur].append(f"{m.group(1)}={m.group(2)}"); continue
    m = re.search(r"console variable '([^']+)' with 'SetBy\w+' was ignored .* previous 'SetBy(\w+)'\. Value remains '([^']*)'", line)
    if m: seen[cur].append(f"{m.group(1)}={m.group(3)} [locked:{m.group(2)}]")
for s in order:
    if '@' in s: print(f"[{s}] " + ' | '.join(seen[s]))
