ECHO off

color f0

:Menu
cls

Title calculator

ECHO ================================
ECHO =                              =
ECHO =         Calculadora          =
ECHO =                              =
ECHO ================================

Echo .
Echo .
Echo 1. Sumar
Echo 2. Restar
Echo 3. Multiplicar
Echo 4. Dividir
Echo 5. Salir
Echo .
Echo .

Set /p Símbolo=Escribe el numero de la operacion: 

if %Símbolo%== 1 goto Sumar
if %Símbolo%== 2 goto Restar
if %Símbolo%== 3 goto Multiplicar
if %Símbolo%== 4 goto Dividir
if %Símbolo%== 5 goto Salir else goto Error



:Error
cls
ECHO ================================
ECHO =                              =
ECHO =            Error             =
ECHO =                              =
ECHO ================================
Echo.
ECHO Elige una opcion valida bobo
ECHO Pulse una tecla para volver al menu: 
PAUSE > nul

goto Menu



:Sumar
cls
Title Calculadora-Sumar

ECHO ================================
ECHO =                              =
ECHO =            Sumar             =
ECHO =                              =
ECHO ================================
Echo.

Set /p Num1=Escribe primer numero: 
Echo
Set /p Num2=Escribe Segundo numero: 
Echo.
Echo -------------------------------
Echo.
Set /a ress=%Num1%+%Num2%
ECHO Da: %ress%
Echo .
Echo Pulsa una tecla para volver al menu: 
PAUSE > nul

goto Menu


:Restar
cls
Title Calculadora-Restar

ECHO ================================
ECHO =                              =
ECHO =           Restar             =
ECHO =                              =
ECHO ================================
Echo.

Set /p Num1=Escribe primer numero: 
Echo
Set /p Num2=Escribe Segundo numero: 
Echo.
Echo -------------------------------
Echo.
Set /a ress=%Num1%-%Num2%
ECHO Da: %ress%
Echo .
Echo Pulsa una tecla para volver al menu: 
PAUSE > nul
goto Menu



:Multiplicar
cls
Title Calculadora-Multiplicar

ECHO ================================
ECHO =                              =
ECHO =         Multiplicar          =
ECHO =                              =
ECHO ================================
Echo.

Set /p Num1=Escribe primer numero: 
Echo
Set /p Num2=Escribe Segundo numero: 
Echo.
Echo -------------------------------
Echo.
Set /a ress=%Num1%*%Num2%
ECHO Da: %ress%
Echo .
Echo Pulsa una tecla para volver al menu: 
PAUSE > nul
goto Menu



:Dividir
cls
Title Calculadora-Dividir

ECHO ================================
ECHO =                              =
ECHO =           Dividir            =
ECHO =                              =
ECHO ================================
Echo.

Set /p Num1=Escribe primer numero: 
Echo
Set /p Num2=Escribe Segundo numero: 
Echo.
Echo -------------------------------
Echo.
Set /a ress=%Num1%/%Num2%
ECHO Da: %ress%
Echo .
Echo Pulsa una tecla para volver al menu: 
PAUSE > nul
goto Menu