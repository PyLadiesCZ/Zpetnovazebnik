## O co jde?

Zpětnovazebník je stránka na které se shromažďují zpětné vazby z jednotlivých lekcí kurzů a workshopů PyLadies https://pyladies.cz/,
Zpětnou vazbu přidávají účastníci a koučové ze "zaheslovaného" odkazu.
Kurz je na Zpětnovazebník možné přidat ručně přes /admin rozhraní, nebo importem celého kurzu z API  https://naucse.python.cz/.


## Instalace a spuštění

* (nepovinné) Vytvoř a aktivuj si [virtuální prostředí](https://naucse.python.cz/lessons/beginners/install/) v Pythonu 3.6.
* Přepni se do adresáře s kódem projektu.
* Nainstaluj závislosti:

  * Linux/Mac:

    ```console
    $ python3 -m pip install pipenv
    $ pipenv install
    ```

  * Windows:

    ```doscon
    > py -3 -m pip install pipenv
    > pipenv install
    ```

Nainstalovanou aplikaci spustíš následovně:

* (nepovinné) Aktivuj si virtuální prostředí, máš-li ho vytvořené.
* Spusť vývojový server:
  ```console
  $ python manage.py runserver
  ```
* Program vypíše adresu (např. `http://127.0.0.1:8000/`); tu navštiv v prohlížeči.

## Licence

Kód je k dispozici pod licencí MIT, viz soubor [LICENSE.MIT].
