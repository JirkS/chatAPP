# chat APP

URL adresa: http://16.16.68.180:5000/<br />

Webová aplikace obsahuje jednoduchou registraci a přihlášení. Pro využívání chat aplikace musíte být přihlášeni a mít správnou autentizaci. Můžete vstupovat do roomek pouze pomocí jejích čísla a zárověň z nich můžete odejít. Můžete posílat zprávy do jednotlivých chatů a číst real-time zprávy ostatních uživatelů.

## Struktura
- Home - uvítací stránka, která vás odkáže na registraci a přihlášení
- Chat APP -> přístup pouze s autentizací a přihlášením, roomky jsou přístupné pouze pomocí zadání čísla dané roomky, které je unikátní
- Login - přihlášení pomocí emailu a hesla
- Register - registrace pomocí uživatelkého jména, emailu a hesla

## Funkce
- Registrace nového účtu k aplikaci
- Přihlášení zaregistrovaným účtem (tehchnologie: session) 
- Připojování a opouštění chatovacích skupin
- Realtime komunikace (technologie: Socket.IO)
- Odesílání a přijímání zpráv v rámci skupin chatu v reálním čase
- Zobrazování chybných hlášek, při nesprávném užívání v rámci celé webové aplikace
- Ukládání uživatelů a zpráv jednotlivých chatů do databáze (technologie: sql)
- Hashovaní hesla (technologie: hash())
- Loggování infa a errorů rozděleně do dvou souborů.

## Technologie
- python Flask (app.py)
- session implementována
- SocketIO
- MySQL
- RotatingFileHandler

## Web Socket
### Server
#### Připojení do roomu
- využívá předepsanou metodu @socketio.on('join')
- uživatel je vpuštěn do určité roomky a bot vypíše do chatu, že uživatel se připojil
- z databáze se načtou zprávy

#### Opuštění roomu
- využívá předepsanou metodu @socketio.on('leave')
- uživatel je odebrán z určité roomky a bot vypíše do chatu, že uživatel se odpojil

#### Posílání a čtení zpráv
- využívá předepsanou metodu @socketio.on('message')
- z databáze se načtou veškeré zprávy z dané roomky

### Klient
#### Připojení do roomu
- uživatel klikne na tlačítko "Join room" a javascript metoda si načte vše potřebné a posílá request na server na join

#### Opuštění roomu
- uživatel klikne na tlačítko "Leave room" a javascript metoda si načte vše potřebné a posílá request na server na leave

#### Posílání zpráv
- uživatel klikne na tlačítko "send" a javascript metoda si načte vše potřebné a posílá request na server na message

#### Čtení zpráv
- server pokaždé co je odeslána nová zpráva, načte si předešlé zprávy pomocí metody load messages s využitím socketu

## REST API Endpointy
### 1. Získání všech zpráv ze všech chat roomů.
- URL: /chat-api/
- Metoda: GET
- Potřeba Autentizace: YES
- Odpověď: JSON

### 2. Zobrazení všech zpráv od vybraného uživatele.
- URL: /chat-api/name
- Metoda: GET
- Potřeba Autentizace: YES
- Odpověď: JSON
  
### 3. Přístup ke všem zprávám z konkrétního chat roomu.
- URL: /chat-api/id
- Metoda: GET
- Potřeba Autentizace: YES
- Odpověď: JSON

### 4. Vyhledání všech zpráv obsahujících vybrané slovo (case insensitive).
- URL: /chat-api/word/word
- Metoda: GET
- Potřeba Autentizace: YES
- Odpověď: JSON

## Autentizace
Aplikace vyžaduje autentizaci pro přístup k některým endpointům. Přidejte hlavičku Authorization s platným JWT tokenem k požadavkům.<br />
"AUTH_TOKEN=kocka"

## Licence
Tato aplikace je poskytována pod licencí MIT License.
