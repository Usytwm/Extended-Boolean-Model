@echo off
echo [Activando entorno virtual...]
call venv\Scripts\activate.bat
echo ----------Completado----------

echo [Instalando dependencias...]
pip install -r requirements.txt
echo ----------Completado----------

echo [Navegando al directorio src...]
cd src
echo ----------Completado----------

@echo off
echo [Ejecutando Server...]
start cmd /k "python proyect_code\main.py & echo ----------Completado---------- & pause"

echo [Ejecutando script de GUI...]
start cmd /k "cd gui/clientapp && npm start & echo ---- & pause"


echo [Regresando al directorio raiz...]
cd ..
echo ----------Completado----------

echo Script finalizado.

