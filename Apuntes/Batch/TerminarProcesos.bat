ECHO off

ECHO Presione cualquier tecla para comenzar el proceso:
PAUSE > nul
REM Comienza el proceso
START wmplayer.exe

ECHO Presione cualquier tecla para terminar el proceso: 
PAUSE > nul
REM /f elimina el proceso a la fuerza

REM TASKLIST para ver procesos

TASKKILL /f /im wmplayer.exe

exit