# Zpětnovazebník

Web pro sbírání zpětné vazby z jednotlivých lekcí kurzů a workshopů PyLadies https://pyladies.cz/,
Zpětnou vazbu přidávají účastníci a koučové ze "zaheslovaného" odkazu.
Kurz je na Zpětnovazebník možné přidat ručně přes /admin rozhraní, nebo importem celého kurzu z API  https://naucse.python.cz/.


## Instalace a spuštění

* Přepni se do adresáře s kódem projektu. 

Nainstalovanou aplikaci spustíš následovně:

* Nainstaluj si [poetry](https://python-poetry.org/docs).
* Nainstaluj závislosti:
  ```console
  $ poetry install
  ```
* Proveď migraci:
  ```console
  $ poetry run python manage.py migrate
  ```
* Spusť vývojový server:
  ```console
  $ poetry run python manage.py runserver
  ```
* Program vypíše adresu (např. `http://127.0.0.1:8000/`); tu navštiv v prohlížeči.

## Testy

Aplikace obsahuje několik testů, které se z nainstalovaného vývojového
prostředí dají spustit pomocí:

```console
$ poetry run python -m pytest
```

## Nasazení

Aplikace jede na [rosti.cz](https://rosti.cz/). Pro nasazení je potřeba:

```bash
cd app
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput 
supervisorctl restart app
```

Při změně závislostí je třeba na vývojářově stroji pustit:

```
poetry update
poetry export -f requirements.txt -o requirements.txt
```

Výsledek se dá do Gitu a v produkci se pustí `pip install -r requirements.txt`.

### První nasazení

Na Roští bylo po vytvoření aplikace potřeba:

- Smazat `/srv/app` a nahradit klonem repozitáře
- V `/srv/conf/supervisor.d/python.conf` změnit jméno modulu s aplikací
  (na konci přík. řádky pro gunicornn) na `feedback.wsgi`
- V `/srv/conf/nginx.d/app.conf` přidat místo zakomentované ukázky:
  ```
        location /static/ {
                alias /srv/app/staticfiles/;
        }
  ```

## Licence

Kód je k dispozici pod licencí MIT, viz soubor [LICENSE.MIT].
