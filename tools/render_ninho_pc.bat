@echo off
rem Renderiza as fotos 3D da Ninho Alto no PC com placa NVIDIA (OptiX). Duplo clique e espere.
rem Saida: saida\ninho\*.png  |  log: saida\ninho\render.log
cd /d "%~dp0"
if exist "blender\ninho_produto.py" (set R=%~dp0) else (cd .. & set R=%~dp0..\)
cd /d "%R%"
set B=
for /d %%D in ("C:\Program Files\Blender Foundation\Blender*") do if exist "%%D\blender.exe" set "B=%%D\blender.exe"
if "%B%"=="" (echo Blender nao encontrado em C:\Program Files\Blender Foundation & pause & exit /b 1)
if not exist saida\ninho mkdir saida\ninho
echo Usando %B% > saida\ninho\render.log
"%B%" -b -P blender\ninho_produto.py -- --cena hero --res 2400 --amostras 256 --gpu --saida saida/ninho/hero_ >> saida\ninho\render.log 2>&1
for %%L in (reserve sunrise night) do "%B%" -b -P blender\ninho_produto.py -- --cena pacote --lote %%L --res 1400 --proporcao 4:5 --amostras 256 --gpu --saida saida/ninho/pacote_%%L_ >> saida\ninho\render.log 2>&1
"%B%" -b -P blender\ninho_produto.py -- --cena graos --res 1800 --amostras 256 --gpu --saida saida/ninho/graos_ >> saida\ninho\render.log 2>&1
echo PRONTO >> saida\ninho\render.log
echo Pronto. Imagens em saida\ninho
