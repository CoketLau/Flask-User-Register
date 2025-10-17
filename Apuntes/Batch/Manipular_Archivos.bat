ECHO off

COPY "C:\Users\alumno\Documents\Tareas\Infografia_SO_Lauret Torres_Adriano.pdf" "C:\Users\alumno\Documents"

ECHO Move new file to "Tareas?"
PAUSE
ECHO Delete first file?
PAUSE

DEL "C:\Users\alumno\Documents\Tareas\Infografia_SO_Lauret Torres_Adriano.pdf"
MOVE "C:\Users\alumno\Documents\Infografia_SO_Lauret Torres_Adriano.pdf" "C:\Users\alumno\Documents\Tareas"

EXIT