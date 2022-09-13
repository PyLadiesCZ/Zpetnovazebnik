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

## Licence

Kód je k dispozici pod licencí MIT, viz soubor [LICENSE.MIT].
