# AI-Driven Behavior Driven Development: Ein technischer Leitfaden für die Software-Entwicklung

**Version: 1.4.0**

## Präambel

Die vorliegenden Richtlinien definieren den standardisierten Prozess für die Software-Entwicklung. Sie markieren einen Paradigmenwechsel von der klassischen Programmierung hin zu einer spezifikationsgetriebenen Entwicklung, bei der Künstliche Intelligenz als exekutives Werkzeug fungiert. In diesem Modell ist das Feature-File, formuliert in der Gherkin-Syntax, die alleinige Quelle der Wahrheit ("Single Source of Truth").

## 1. Die Natur des ausführbaren Vertrags

Die fundamentale Prämisse unseres Ansatzes lautet, dass eine Software- Lösung vollständig durch ihr von außen beobachtbares Verhalten definiert ist. Das Feature-File dient hierbei als bindender Vertrag zwischen der fachlichen Anforderung und der technischen Umsetzung. Wir erzwingen eine strikte Synchronisation: Das Feature-File ist der deterministische Prompt für den KI-Agenten.

## 2. Explizitheit und Transparenz der Daten (Single Source of Truth)

Ein kritisches Qualitätsmerkmal dieses Prozesses ist die vollständige Transparenz von Daten und Konfigurationen. Ein häufiges Anti-Pattern in der herkömmlichen BDD-Praxis ist das Verbergen von Parametern innerhalb der Step-Implementierungen ("Glue Code"). Dies führt zu "magischen Werten", die im Gherkin-Text unsichtbar sind, und untergräbt den Wert der Spezifikation.

### 2.1 Fallstudie: Vermeidung impliziter Konfiguration (Referenz: DDNS Service)

Betrachten wir einen **Dynamic DNS Service**, der auf einem bestimmten Netzwerk-Port lauschen und mit einer externen API kommunizieren muss. In einer robusten Architektur dürfen diese Parameter nicht im Programmcode hardcodiert sein. Sie müssen explizit im Szenario ausgewiesen werden, damit das Verhalten auch ohne Einsicht in den Code verständlich ist.

**Positiv-Beispiel (Explizite Konfiguration):**
Hier dient das Feature-File als alleinige Konfigurationsquelle. Der Code wird zu einer generischen Schicht, die lediglich die Daten aus der Tabelle anwendet.

*Feature File:*
```gherkin
Given the ddns-service is configured with:
  | key                  | value                 |
  | listen-port          | 8080                  |
  | autodns-api-base-url | http://localhost:8081 |
```

**Technische Umsetzung (Vom Gherkin zum CLI-Aufruf):**
Der Python-Step liest diese Tabelle und konstruiert daraus dynamisch die Argumente für den Start des Services. Es gibt keine "versteckte Wahrheit" im Python-Code; alle Laufzeitparameter stammen direkt aus dem Feature-File.

```python
@given("the ddns-service is configured with")
def step_impl(context):
    if not hasattr(context, 'ddns_config'):
        context.ddns_config = {}

    for row in context.table:
        context.ddns_config[row['key']] = row['value']

@given("the ddns-service is listening")
def start_service(context):
    cmd = ["./bin/ddns-service"]
    # Generiere CLI-Flags dynamisch: 
    # Aus {'listen-port': '8080'} wird ["--listen-port=8080"]
    for key, value in context.ddns_config.items():
        cmd.append(f"--{key}={value}")
    
    # Resultierender Befehl:
    # ./bin/ddns-service --listen-port=8080 --autodns-api-base-url=http://localhost:8081
    context.process = subprocess.Popen(cmd)
```

**Konsequenz & Fazit:**
Die Tests erzwingen, dass die Applikation vollständig über die Kommandozeile konfigurierbar ist. Es gibt keine hardcodierten Konstanten für Ports oder URLs im Code, da der Test sonst nicht funktionieren würde. Die **CLI-Schnittstelle wird durch den Test definiert**.

### 2.2 Die Gefahr von Datenlücken (Requirement Gaps)

Ein kritisches Versagen im Test-Design tritt auf, wenn im Erwartungshorizont (`Then`) Daten gefordert werden, die in der Datenbasis (`Given`) nicht enthalten sind. Dies erzeugt eine logische Lücke, die die technische Umsetzung korrumpiert: Der Entwickler (oder der KI-Agent) wird gezwungen, "magische Werte" hart zu kodieren, um den Test zu bestehen. 

Ein valider BDD-Test muss eine **reine Transformation** (Pure Function) darstellen. Jeder Wert, der im `Then`-Schritt validiert wird, muss entweder:
1.  Direkt aus dem `Given`-Schritt stammen.
2.  Durch eine im Feature-File explizit beschriebene Business-Regel aus den Eingangsdaten abgeleitet werden.

**Anti-Pattern (Datenlücke):**
Das Szenario erwartet eine spezifische IBAN und Steuer-Codes im Ergebnis, liefert diese aber nicht im Input mit.

*Schlechtes Feature File:*
```gherkin
Scenario: Map Order to Marketplace
    Given an order for item "X"
    When the mapping logic is applied
    Then the output must contain:
      | field | value       |
      | iban  | DE123456789 |  <-- Woher kommt dieser Wert?
      | tax   | VAT_DE      |  <-- "Magisches" Wissen
```

**Konsequenz:**
Der resultierende Code wird diesen Wert fest verdrahten (`const IBAN = "DE123456789"`). Der Test ist damit wertlos, da er keine allgemeingültige Logik prüft, sondern nur die Übereinstimmung zweier statischer Texte.

**Best Practice (Anti-Hardcoding Strategie):**
1.  **Vollständigkeit:** Ergänzen Sie den `Given`-Block um alle notwendigen Quelldaten.
2.  **Varianz (Der "Bob-Test"):** Erstellen Sie immer mindestens zwei Szenarien (z.B. mittels `Scenario Outline`) mit unterschiedlichen Werten für dieselben Felder. Wenn die Implementierung einen Wert hardcodiert hat, wird das zweite Szenario zwangsläufig fehlschlagen. Nur so lässt sich beweisen, dass die Logik tatsächlich **generisch** arbeitet.

### 2.3 Trennung von Stamm- und Bewegungsdaten

Bei komplexen Geschäftsobjekten (z.B. Rechnungen) sollten statische Konfigurationen (Stammdaten) von fallbezogenen Daten (Bewegungsdaten) getrennt werden.

*   **Stammdaten (Issuer Config):** Diese sollten **explizit** im `Given`-Block als JSON/DocString definiert werden. Dies schafft Transparenz über die Konfiguration des Systems ("Wer bin ich?").
*   **Bewegungsdaten (Invoice Data):** Diese können ebenfalls explizit übergeben oder - wenn der Fokus auf der Verarbeitung echter Artefakte liegt - referenziert werden ("Given the invoice data matches 'invoice_01.json'").

Dies verhindert, dass Feature-Files durch die Wiederholung statischer Daten unlesbar werden, ohne die Anforderung der Vollständigkeit zu verletzen.

## 3. Komplexe Datenstrukturen und Payloads

Für Enterprise-Anwendungen reicht die Übergabe einfacher Schlüssel-Wert-Paare oft nicht aus. Komplexe Geschäftsobjekte, JSON-Payloads oder Datenbank-Schemata müssen mittels **DocStrings** (Triple-Quotes) direkt im Szenario abgebildet werden. Dies stellt sicher, dass auch komplexe Validierungslogik für Fachexperten lesbar bleibt.

### 3.1 Fallstudie: Business-Objekte (Referenz: PaperSink DMS)

Anstatt die Validierungslogik für Pflichtfelder wie `net_amount` oder `currency` im Code zu vergraben, wird das erwartete Datenobjekt als JSON im Gherkin definiert.

*Feature File:*
```gherkin
Scenario: Upload a valid Invoice document
    And the client provides business metadata:
      """
      {
        "invoice_number": "INV-2025-001",
        "net_amount": 10050,
        "currency": "EUR"
      }
      """
```

**Technische Umsetzung (DocString Parsing):**
Der Step-Code parst den DocString und nutzt ihn direkt für den API-Request.

```python
@given("the client provides business metadata")
def step_impl(context):
    try:
        # Validierung, dass der DocString valides JSON ist
        metadata = json.loads(context.text)
        context.request_payload = metadata
    except json.JSONDecodeError as e:
        raise AssertionError(f"Invalid JSON in Feature File: {e}")

@when("the client sends the document")
def send_document(context):
    # Das JSON aus dem Feature File wird 1:1 an die API gesendet
    requests.post(url, json=context.request_payload)
```

**Konsequenz & Fazit:**
Das Feature-File wird zur **Schema-Referenz**. Es gibt keine impliziten Default-Werte im Test-Code. Dies zwingt die API dazu, fehlende Pflichtfelder (z.B. wenn `currency` im Gherkin weggelassen wird) korrekt zu behandeln (z.B. 400 Bad Request), anstatt dass der Test-Code diese heimlich auffüllt.

### 3.2 Fallstudie: Transformations-Logik (Referenz: Enterprise Integration)

In komplexen Integrationsszenarien besteht die Kernaufgabe oft darin, Daten von einem Quellsystem (z.B. Shop-API) in ein Zielsystem (z.B. ERP) zu mappen. Diese Mappings sind reine Geschäftslogik und dürfen nicht tief im Java- oder Go-Code versteckt sein.

*Feature File:*
```gherkin
Scenario: Mapping of custom fields from Source System to Target System
  # Definition der Eingangsdaten (Quellsystem)
  Given a source order with custom fields:
    | source_code | value      |
    | color-01    | blue       |
    | size-x      | 42         |
  
  When the order mapping logic is applied
  
  # Definition der erwarteten Ausgangsdaten (Zielsystem)
  Then the target system structure should contain:
    | target_field   | value |
    | attributes.col | blue  |
    | attributes.sz  | 42    |
```

**Technische Umsetzung (Unit-Level BDD):**
Hier wird kein HTTP-Request gesendet, sondern die Mapping-Funktion der Applikation direkt aufgerufen.

```python
@when("the order mapping logic is applied")
def step_impl(context):
    from src.logic import mapper
    context.target_order = mapper.transform(context.source_order)

@then("the target system structure should contain")
def step_impl(context):
    for row in context.table:
        actual = get_value(context.target_order, row['target_field'])
        assert actual == row['value']
```

**Konsequenz & Fazit:**
Geschäftslogik wird für Fachexperten **lesbar und validierbar**. Komplexe Mappings sind nicht mehr in Java-Streams oder Go-Loops versteckt, sondern stehen explizit als Beispiele im Gherkin. Dies verhindert "Lost in Translation"-Fehler zwischen Business und IT.

### 3.3 Fallstudie: Observability & Logging (Referenz: DDNS Service)

Oft ist der interne Zustand eines Systems von außen nur schwer einsehbar.

*Feature File:*
```gherkin
Scenario: Successful update produces a structured JSON log
    And the service should log the following structured JSON message:
      """
      {
        "level": "info",
        "message": "Successfully updated DNS record",
        "service": "ddns-service",
        "context": {
          "dns_name": "gupta.ddns.scaratec.com",
          "update_ip": "127.0.0.1"
        }
      }
      """
```

**Technische Umsetzung (Log Capture):**
Der Step-Code liest den `stdout` des Subprozesses und parst jede Zeile als JSON.

```python
@then("the service should log the following structured JSON message")
def step_impl(context):
    expected_log = json.loads(context.text)
    logs = get_captured_logs(context)
    assert any(is_subset(expected_log, log) for log in logs)
```

**Konsequenz & Fazit:**
Logging wird zum **First-Class Feature**. Der Test erzwingt, dass die Applikation strukturierte, maschinenlesbare Logs (JSON) schreibt, anstatt unstrukturierte Textwüsten. Dies garantiert die Integrierbarkeit in Monitoring-Systeme (ELK, Splunk) ab Tag 1.

### 3.4 Umgang mit Legacy-Daten (Garbage In)

Wenn Systeme unstrukturierte oder unsichere Eingaben (z.B. OCR von Word-PDFs) verarbeiten müssen, definieren Sie Szenarien für den "Sad Path" explizit.

*   **Trennungsprinzip:** Trennen Sie den unsicheren Extraktor ("Rate mal was das ist") vom sicheren Generator ("Erzeuge valides Ergebnis aus validen Daten").
*   **Test-Fokus:** Testen Sie den Generator (Core-Logik) nur mit validen oder explizit invaliden (aber strukturierten) Daten, um "Flaky Tests" durch unzuverlässige OCR zu vermeiden.
*   **Fail Fast:** Legen Sie im Test fest, dass bei Inkonsistenzen (z.B. fehlende Pflichtfelder nach der Extraktion) der Prozess kontrolliert abbricht, statt invalide Ergebnisse zu produzieren.

## 4. Technische Isolation und Architektur

Um die Integrität der Validierung zu gewährleisten, ist eine strikte Trennung zwischen der Test-Infrastruktur und dem Produktionssystem erforderlich.

### 4.1 Isolierte Laufzeitumgebung

Das BDD-Framework operiert in einer vollständig isolierten Umgebung (`.venv`), die keine Abhängigkeiten mit dem Produktionscode teilt. **Diese strikte Trennung gilt zwingend auch dann, wenn sowohl die Applikation als auch die Test-Suite in Python implementiert sind.**

### 4.2 Modularisierung der Steps (Referenz: MOIS2)

Mit steigender Komplexität des Systems muss auch die Struktur der Validierung skalieren. Monolithische Step-Dateien sind zu vermeiden.

*Empfohlene Struktur:*
```text
bdd/steps/
├── ingress_steps.py    # Behandelt HTTP-Eingänge und API-Aufrufe
├── logic_steps.py      # Validiert interne Geschäftsregeln und Transformationen
└── cloud_steps.py      # Simuliert Infrastruktur-Events (z.B. PubSub Nachrichten)
```

## 5. UI-Testing und Browser-Automatisierung (New in 1.4.0)

Beim Testen von grafischen Oberflächen (Web-UIs) treten spezifische Herausforderungen auf, die eine Erweiterung der BDD-Methodik erfordern.

### 5.1 Das Verbot des "Zirkelschlusses" (Avoid "Testing the Test")

Ein kritischer Fehler in der Test-Automatisierung ist die Re-Implementierung von Applikationslogik innerhalb der Test-Steps. Dies führt dazu, dass der Test "blind" wird: Er bestätigt seine eigene (potenziell falsche) Logik, anstatt das tatsächliche Verhalten der Applikation zu validieren.

*   **Anti-Pattern:** Der Test-Step berechnet die Brutto-Summe aus den Eingabedaten selbst und vergleicht sie mit einem intern generierten JSON.
*   **Best Practice:** Der Test-Step ist "dumm". Er trägt Werte in die UI ein und liest ausschließlich die *Labels* oder *Zustände* aus, die die Applikation im DOM erzeugt hat.

**Wahrheitsgehalt:** "Wenn die UI behauptet, das Ergebnis sei X, dann validieren wir gegen X. Wir berechnen X niemals im Test-Code neu."

### 5.2 Event-Handling und Benutzer-Simulation

Moderne Web-Frameworks reagieren auf Benutzerinteraktionen (Events wie `input`, `change`, `click`). Programmatisches Setzen von Werten (z.B. `element.value = '123'`) löst diese Events im Browser oft **nicht** aus.

*   **Strategie:** Bevorzugen Sie Low-Level Benutzer-Simulationen (z.B. `page.type()` oder `element.press()`), anstatt Eigenschaften direkt zu manipulieren.
*   **Fallback:** Wenn Werte direkt gesetzt werden müssen, müssen die entsprechenden Events explizit via JavaScript getriggert werden, um die Reaktionskette der Applikation (z.B. automatische Summenberechnung) anzustoßen.

### 5.3 Isolation gegen Caching und State-Leakage

Browser-Caching und persistente Sessions können Testergebnisse verfälschen.

*   **Sauberer Start:** Jedes Szenario (oder zumindest jedes Feature) muss in einem vollständig isolierten Browser-Kontext (`Incognito` / `isolatedContext`) starten.
*   **Port-Wächter:** Stellen Sie sicher, dass keine "Geister-Prozesse" (alte Server-Instanzen) auf den Test-Ports lauschen. Automatisierte Housekeeping-Skripte (z.B. im `Makefile` oder `environment.py`) müssen sicherstellen, dass vor Testbeginn die Umgebung "sauber" ist.

### 5.4 Fallstudie: UI-Interaktion (Referenz: Osthues Insight Engine)

*Feature File:*
```gherkin
Scenario: Candidate Selection in Data Grid
    When the user selects the candidate "Max Mustermann" in the data grid
```

**Technische Umsetzung (Selenium/Puppeteer Abstraktion):**
Der Step-Code kapselt die Komplexität der Browser-Automatisierung.

```python
@when('the user selects the candidate "{name}" in the data grid')
def step_impl(context, name):
    xpath = f"//div[@role='row' and contains(., '{name}')]"
    row = context.driver.find_element(By.XPATH, xpath)
    row.click()
```

**Konsequenz & Fazit:**
Tests werden **resilient gegen Layout-Änderungen**. Da das Gherkin nur die Intention ("Wähle Kandidat") beschreibt, muss bei einer Änderung des HTML-Gerüsts (z.B. neue CSS-Klasse) nur der eine Python-Step angepasst werden, nicht hunderte Testszenarien.

## 6. Architecture by Design: Ports & Adapters

Feature Files können genutzt werden, um architektonische Kapselung zu erzwingen.

### 6.1 Fallstudie: Kapselung von API-Clients (Referenz: AutoDNS Library)

Indem wir ein Feature-File schreiben, das *nur* eine Library testet (und nicht den ganzen Service), zwingen wir den Entwickler dazu, diesen Code sauber vom Rest der Anwendung zu trennen.

*Feature File (Library Test):*
```gherkin
@library @autodns
Feature: AutoDNS Library Integration
  Scenario: Library successfully authenticates
    When I run the AutoDNS library test "login" command with:
      | arg       | value |
      | user      | user  |
```

### 6.2 Fallstudie: Hexagonale Architektur (Referenz: PaperSink)

Wenn wir Software spezifizieren, die unabhängig von ihrer Infrastruktur (Datenbank, Cloud-Provider) testbar sein soll, führt der Weg fast zwangsläufig zur **Hexagonalen Architektur (Ports and Adapters)**. BDD unterstützt dies natürlich, da der Test den "Treiber" (Primary Adapter) spielt und Mocks die "Getriebenen" (Secondary Adapters) ersetzen.

**Struktureller Beweis:**
Im Projekt `papersink` sehen wir diese Trennung physisch im Dateisystem:

```text
/internal
├── core/
│   ├── domain/       # Reine Geschäftslogik (Entities)
│   └── ports/        # Interfaces (Was braucht der Core?)
│       └── ports.go  # "type DocumentRepository interface {...}"
└── adapter/
    ├── firestore/    # Konkrete Implementierung (Google Cloud)
    └── http/         # REST API Handler
```

## 7. Strategien für externe Abhängigkeiten (Mocking & Infrastruktur)

Moderne Systeme interagieren mit komplexen Infrastrukturen. In unserer BDD-Methodik nutzen wir deterministische Mocks.

### 7.1 Deklaratives Mocking mit Mockoon (Referenz: DDNS Service)

HTTP-Abhängigkeiten werden über Mock-Server gesteuert, deren Konfiguration im Feature-File referenziert wird.

### 7.2 Infrastruktur-Mocking: PKI & DNS (Referenz: DDNS Service)

Sogar systemnahe Komponenten wie Verschlüsselung (TLS) können spezifiziert werden.

### 7.3 AI-Accelerated Mocking: Ad-hoc System-Repliken

Durch den Einsatz von AI Agents können Nachbarsysteme **Ad-hoc** als Mocks generiert werden.

### 7.4 Resilient Testing: Eventual Consistency Patterns

In verteilten Cloud-Systemen ist "Sofortigkeit" eine Illusion. Operationen wie das Propagieren von Secrets, das Starten von Containern (Cold Starts) oder das Zustellen von Nachrichten (Pub/Sub) benötigen Zeit. Tests, die Zustände *einmalig* prüfen und bei einem Fehler sofort abbrechen, führen zu "Flaky Tests".

**Strategie: Polling mit Timeout**
Statt eines einfachen `assert` nutzen wir eine Retry-Schleife. Der Test gilt erst dann als gescheitert, wenn der gewünschte Zustand nach Ablauf einer definierten Zeitspanne (z.B. 60 Sekunden) nicht eingetreten ist.

## 8. Der iterative Prozess (Red/Green)

Die Entwicklung folgt einem strikten iterativen Prozess.

1.  **Red State:** Anforderung im Feature-File formulieren -> `behave` scheitert.
2.  **Implementation:** KI generiert Code (App + Steps).
3.  **Green State:** `make test` läuft durch.

## 9. Beweisführung und Incident-Analyse durch BDD

BDD ist nicht nur ein Entwicklungswerkzeug, sondern auch ein mächtiges Instrument zur **Ursachenanalyse und Beweisführung** (Forensic Engineering) in komplexen, verteilten Systemen.

### 9.1 Reproduktion von "Heisenbugs" (Referenz: Checkout-Service)

BDD ermöglicht es, sporadische Bedingungen (Race Conditions) deterministisch nachzustellen.

### 9.2 Der Test als Beweisstück

Ein fehlschlagender BDD-Test ist der ultimative Beweis für die Existenz eines Bugs und dessen Ursache.

### 9.3 Aufdeckung von "Silent Failures"

Ein "Silent Failure" liegt vor, wenn das System dem Benutzer (UI) Erfolg signalisiert, aber im Hintergrund (DB/API) keine Datenpersistenz stattfindet.

*   **BDD-Ansatz:** Ein Test darf niemals nur den HTTP-Statuscode des Redirects prüfen. Er muss zwingend den Zustand des Zielsystems validieren.

## Schlusswort

Die Qualität des Software-Produkts korreliert direkt mit der Präzision der Feature-Files. Indem wir Infrastruktur, Daten und Architektur in die Spezifikation heben, schaffen wir Systeme, die durch KI deterministisch reproduzierbar sind.
