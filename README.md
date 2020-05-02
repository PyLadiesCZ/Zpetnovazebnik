# Zpětnovazebník

Web pro sbírání zpětné vazby z jednotlivých lekcí kurzů a workshopů PyLadies https://pyladies.cz/,
Zpětnou vazbu přidávají účastníci a koučové ze "zaheslovaného" odkazu.
Kurz je na Zpětnovazebník možné přidat ručně přes /admin rozhraní, nebo importem celého kurzu z API  https://naucse.python.cz/.


## Instalace a spuštění

* Přepni se do adresáře s kódem projektu. 

Nainstalovanou aplikaci spustíš následovně:

* (nepovinné) Aktivuj si virtuální prostředí, máš-li ho vytvořené.
* Nainstaluj závislosti:
  ```console
  $ python -m pip install -r requirements-local.txt
  ```
* Proveď migraci:
  ```console
  $ python manage.py migrate
  ```
* Spusť vývojový server:
  ```console
  $ python manage.py runserver
  ```
* Program vypíše adresu (např. `http://127.0.0.1:8000/`); tu navštiv v prohlížeči.

## Testy

Aplikace obsahuje několik testů, které se z nainstalovaného vývojového
prostředí dají spustit pomocí:

```console
$ python -m pytest
```

## Licence

Kód je k dispozici pod licencí MIT, viz soubor [LICENSE.MIT].
