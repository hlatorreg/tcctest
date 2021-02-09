## Instalación

Despues de clonar crea un ambiente virtual con pyenv e instala las dependencias

```shell
$ pyenv local 3.9.0
$ python -m venv venv --prompt tcchallenge
$ source venv/bin/activate
$ pip install -r requirements.txt
```

No es necesario correr migraciones ya que los modelos se mantienen igual
En una terminal levanta el proyecto con

```shell
$ python manage.py runserver
```

- http://127.0.0.1:8000/assetdata/BTC Lista los datos segun lo indicado, la ultima parte de la ruta es el nombre del asset y es variable
- http://127.0.0.1:8000/assets/ Permite crear assets
- http://127.0.0.1:8000/asset/<int:id> Permite updatear o destruir assets
- http://127.0.0.1:8000/scrapers/ Permite crear scrapers
- http://127.0.0.1:8000/scraper/<int:id> Permite updatear o destruir assets

### Para crear otro scraper se debe crear un asset primero

### Para correr un scraper corremos el comando

```shell
$ python manage.py crawl -scraper <SCRAPER_ID>
```

Un error se desplegará si el scraper no está activo o el ID no existe o es distinto a un entero positivo.