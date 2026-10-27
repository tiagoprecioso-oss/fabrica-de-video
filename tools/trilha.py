"""Gera a trilha de um vídeo da fábrica a partir do JSON: batida que fecha no loop, acordes de fundo,
'whoosh' nas transições e brilho nos selos. Sem som de legenda.
Uso: python3 tools/trilha.py videos/<id>.json"""
import json, sys, wave
import numpy as np

v = json.load(open(sys.argv[1]))
DUR = v["duracao"]; BEAT = DUR / v.get("batidas", round(DUR / (60 / 104)))
SR = 44100; L = int(DUR * SR); mix = np.zeros(L, np.float32)
tt = lambda s: np.arange(int(s * SR)) / SR
def add(sig, at, g=1.0):
    i = int(at * SR); j = min(L, i + len(sig))
    if 0 <= i < L: mix[i:j] += sig[: j - i] * g

kick = np.sin(2 * np.pi * (50 + 120 * np.exp(-tt(.35) * 30)) * tt(.35)) * np.exp(-tt(.35) * 9)
hat = np.random.default_rng(1).normal(0, 1, len(tt(.06))) * np.exp(-tt(.06) * 70)
nz = np.random.default_rng(2).normal(0, 1, len(tt(.45)))
whoosh = np.convolve(nz * np.sin(np.pi * np.linspace(0, 1, len(nz))) ** 2, np.ones(40) / 40, "same")
brilho = sum(np.sin(2 * np.pi * f * tt(.7)) for f in (1318, 1661, 1976)) * np.exp(-tt(.7) * 5) / 3
def pad(freqs, dur):
    x = tt(dur); s = sum(np.sin(2 * np.pi * f * x) + .5 * np.sin(2 * np.pi * f * 2.003 * x) for f in freqs)
    return s * np.minimum(1, x / .4) * np.minimum(1, (dur - x) / .4) / len(freqs)

acordes = [(220, 261.6, 329.6), (174.6, 220, 261.6), (196, 246.9, 293.7), (164.8, 207.7, 246.9)]
compasso = BEAT * 4
for k in range(int(DUR / compasso) + 1): add(pad(acordes[k % 4], compasso), k * compasso, .10)
for k in range(int(round(DUR / BEAT))):
    b = k * BEAT
    if b > DUR - .05: break
    add(kick, b, .5); add(hat, b + BEAT / 2, .10)
    nota = [55, 55, 43.65, 49][(k // 4) % 4]
    add(np.sin(2 * np.pi * nota * tt(BEAT * .9)) * np.exp(-tt(BEAT * .9) * 2.5), b, .26)
for b in v["blocos"]:
    if b.get("entrada") == "whip": add(whoosh, b["de"] - .22, .35)
    if b.get("saida") == "loop": add(whoosh, b["ate"] - .32, .35)
    if b.get("selo"): add(brilho, b["selo"]["em"], .45)
mix = mix / max(1e-6, np.abs(mix).max()) * .85
f = int(.04 * SR); mix[:f] *= np.linspace(0, 1, f); mix[-f:] *= np.linspace(1, 0, f)
out = "public/" + v["trilha"]
with wave.open(out, "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print("trilha:", out)
