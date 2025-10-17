Echo off

REM Se le pone el nombre de la variable junto al valor
REM Lo básico es: Set Name= Lauret

REM Requiere de ECHO on

Set /p Name=Escriba su nombre: 

REM Para llamar la variable se pone entre %%

ECHO Hi %Name%!