"""Parse `dumpsys SurfaceFlinger --timestats -dump` for the WuWa game layer.

Prints avg fps, frame count and present-to-present percentiles (ms), plus the
1% low fps. Histogram lines look like `present2present histogram is as below:`
followed by `0ms=0 1ms=0 ... 16ms=120 ...`.
"""
import re
import sys

raw = open(sys.argv[1], encoding="utf-8", errors="replace").read()
blocks = re.split(r"\n(?=layerName = )", raw)
game = [b for b in blocks if b.startswith("layerName = ") and "GameActivity" in b.split("\n", 1)[0]]
if not game:
    print("no game layer in timestats; layers:", [b.split("\n", 1)[0] for b in blocks if b.startswith("layerName")][:5])
    sys.exit(1)
b = max(game, key=lambda x: int(re.search(r"totalFrames = (\d+)", x).group(1)))


def field(name):
    m = re.search(rf"{name} = ([\d.]+)", b)
    return m.group(1) if m else "?"


m = re.search(r"present2present histogram is as below:\n([^\n]*)", b)
hist = {}
if m:
    for k, v in re.findall(r"(\d+)ms=(\d+)", m.group(1)):
        if int(v):
            hist[int(k)] = int(v)
n = sum(hist.values())


def pct(p):
    acc = 0
    for k in sorted(hist):
        acc += hist[k]
        if acc >= p * n:
            return k
    return None


p50, p95, p99 = pct(0.50), pct(0.95), pct(0.99)
low1 = round(1000 / p99, 1) if p99 else "?"
print(f"avgFPS={field('averageFPS')} frames={field('totalFrames')} p50={p50}ms p95={p95}ms p99={p99}ms 1%low~{low1}fps")
