# Sistema de Gestion Presupuestaria (Coop Safa)

El proyecto esta usando python 3.8.8

## Clonar Proyecto
```
git clone https://github.com/CoopsafaIT/PresupuestoMaestro ppto-safa
```

## Instalación
```
cd ppto-safa
python -m virtualenv .venv
.venv/Scripts/activate
pip install -r requirements.txt
pip install python_ldap-3.3.1-cp38-cp38-win_amd64.whl
touch .env (ver .env.example para ver las variables usadas)
python manage.py migrate
python manage.py create_permissions
python manage.py runserver (para correr proyecto en local)
```
> Note: `touch .env` es neserario cuando no se cuenta con las variables de entorno.