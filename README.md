# GUIOSPRO FLOSS — Django sin base de datos

Migración inicial de las tres pestañas del proyecto Flexx (`original/main.py`) a Django. Conserva los CSV originales en `data/` y los cálculos implementados en `evaluacion/logic.py`.

**No necesita PostgreSQL, SQLite ni ninguna base de datos.** Django usa sesiones firmadas en cookies del navegador para conservar temporalmente las respuestas entre formularios; estas respuestas no se almacenan en el servidor. No hay sistema de usuarios ni panel admin en esta etapa. Al borrar las cookies o reiniciar la evaluación se pierde el estado de la evaluación. Las cookies de sesión tienen un límite de tamaño, por lo que esta solución es adecuada solo como punto de partida.

## Ejecutar en Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py check
python manage.py runserver
```

Abre http://127.0.0.1:8000/. **No ejecutes `migrate`: no hace falta.**

Para producción, configura una clave secreta distinta y cambia `DJANGO_DEBUG=False`.

## Etapas originales

- Pasos 1 y 2: importancia, importancia relativa y alcance.
- Pasos 3 y 4: evaluación por subfactor y guardado temporal.
- Pasos 5 y 6: ponderación, FODA y recomendaciones.

Esta es una adaptación web de la lógica original, todavía pendiente de comparación integral de resultados con la aplicación Flexx.
