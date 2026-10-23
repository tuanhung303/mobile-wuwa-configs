"""Build config/Scalability.ini: copy Kuro's own higher-tier values into the active sections.

Usage: python3 gen_scalability.py Client.log.txt [out.ini]

Reads a decrypted Client.log (first pass of each section) and drops:
forbidden cvars (forbidden_cvars.txt),
sg.* lines, and cvars locked by ProjectSetting (a scalability section cannot change them).
The plan below targets the levels the menu runs on a REDMAGIC 11 Pro at max menu
settings (check yours with sections.py); edit it if your active levels differ.
"""
import os
import re
import sys

log = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else 'Scalability.ini'
here = os.path.dirname(os.path.abspath(__file__))
forbidden = {l.strip().lower() for l in open(os.path.join(here, 'forbidden_cvars.txt'))
             if l.strip() and not l.startswith('#')}
sec, vals, locked = None, {}, set()
for line in open(log, encoding='utf-8', errors='replace'):
    m = re.search(r"Applying CVar settings from Section \[([^\]]+)\] File \[[^\]]*Scalability", line)
    if m:
        sec = m.group(1) if m.group(1) not in vals else None
        if sec: vals[sec] = {}
        continue
    if 'Applying CVar settings' in line: sec = None; continue
    if not sec: continue
    m = re.search(r"Setting CVar \[\[([^:\]]+):([^\]]*)\]\]", line)
    if m: vals[sec][m.group(1)] = m.group(2).split(';')[0].strip(); continue
    m = re.search(r"console variable '([^']+)' with 'SetByScalability' was ignored .*'SetByProjectSetting'", line)
    if m: locked.add(m.group(1).lower())


skip_by_choice = {'r.motionblurquality'}  # motion blur smears fights at 90 fps


def keep(k):
    kl = k.lower()
    return not (kl in forbidden or kl in locked or kl in skip_by_choice or kl.startswith('sg.') or '?' in k)


plan = {  # active section <- higher tier it copies from
    'PostProcessQuality@2': 'PostProcessQuality@3',
    'EffectsQuality@2': 'EffectsQuality@3',
    'FoliageQuality@2': 'FoliageQuality@3',
    'TextureQuality@2': 'TextureQuality@4',
}
lines = ['; WuWa mobile visual tune v2 (2026-10-23), REDMAGIC 11 Pro / Adreno 840 profile.',
         '; Active levels from Client.log: ViewDistance@2 AA@2 Shadow@3 PostProcess@2 Texture@2 Effects@2 Foliage@2.',
         "; @2 sections get Kuro's own higher-tier values; forbidden cvars left out (ConfigMonitor strips them).", '']
skipped = []
for tgt, src in plan.items():
    lines.append(f'; {tgt} from {src}')
    lines.append(f'[{tgt}]')  # UE4 drops a section whose header line has anything after the ]
    for k, v in vals[src].items():
        if keep(k) and vals.get(tgt, {}).get(k) != v: lines.append(f'{k}={v}')
        elif not keep(k): skipped.append(f'{src}:{k}')
    lines.append('')
lines += ['[ShadowQuality@3]', 'r.ShadowQuality=4', 'r.Shadow.CSM0ShadowPCFQuality=3', 'r.Shadow.CSM1ShadowPCFQuality=3',
          'r.Shadow.CSM2ShadowPCFQuality=3', 'r.Shadow.CSM3ShadowPCFQuality=3', 'r.Shadow.PerObjectShadowMapResolution=1024',
          'r.Shadow.PerObjectResolutionMax=1024', 'r.Shadow.SkeletalMeshLODBias=0', 'r.ShadowMask.Scale=1.0',
          'r.Shadow.RadiusThreshold=0.01', '', '[ViewDistanceQuality@2]', 'r.StaticMeshLODDistanceScale=0.75', '']
open(out, 'w').write('\n'.join(lines))
print('wrote', out)
print('SKIPPED (forbidden/locked):', ', '.join(skipped))
