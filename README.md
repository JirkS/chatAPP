# chat APP

URL adresa: http://16.16.68.180:5000/<br />

Webová aplikace obsahuje jednoduchou registraci a přihlášení. Pro využívání chat aplikace musíte být přihlášeni a mít správnou autentizaci. Můžete vstupovat do roomek pouze pomocí jejích čísla a zárověň z nich můžete odejít. Můžete posílat zprávy do jednotlivých chatů a číst real-time zprávy ostatních uživatelů.

## Struktura
- Home - uvítací stránka, která vás odkáže na registraci a přihlášení
- Chat APP -> přístup pouze s autentizací a příjlášením
- Login - pomocí emailu a hesla
- Register - pomocí uživatelkého jména, emailu a hesla

## Funkce
- Registrace nového účtu k aplikaci
- Přihlášení zaregistrovaným účtem (tehchnologie: session) 
- Připojování a opouštění chatovacích skupin
- Realtime komunikace (technologie: Socket.IO)
- Odesílání a přijímání zpráv v rámci skupin chatu v reálním čase
- Zobrazování chybných hlášek, při nesprávném užívání celé webové aplikace
- Ukládání uživatelů a zpráv jednotlivých chatů do databáze (technologie: sql)
- Hashovaní hesla (technologie: hash())

## Technologie
- python Flask (app.py)
- session implementována
- SocketIO
- MySQL

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
