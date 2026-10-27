"""Folha de revisão: um quadro do meio de cada legenda + primeiro e último quadro, numa imagem só.
O revisor olha uma imagem em vez de dezenas (mais rápido e mais barato).
Uso: python3 tools/folha.py saida/<id>.mp4 videos/<id>.json saida/<id>-revisao.jpg"""
import json, os, subprocess, sys, tempfile

mp4, js, out = sys.argv[1:4]
v = json.load(open(js))
tempos = [0.05] + [(l["de"] + l["ate"]) / 2 for l in v["legendas"]] + [v["duracao"] - 0.04]
tmp = tempfile.mkdtemp()
for i, t in enumerate(tempos):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", mp4, "-frames:v", "1",
                    "-vf", f"scale=270:-1,drawtext=text='{t:.1f}s':x=8:y=8:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.6",
                    f"{tmp}/q{i:02d}.png"], check=True)
cols = 5
linhas = (len(tempos) + cols - 1) // cols
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "1", "-i", f"{tmp}/q%02d.png",
                "-vf", f"tile={cols}x{linhas}:padding=6:color=black", "-frames:v", "1", "-q:v", "3", out], check=True)
print("folha:", out, f"({len(tempos)} quadros)")
