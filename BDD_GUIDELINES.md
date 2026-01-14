# AI-Driven Behavior Driven Development: Ein technischer Leitfaden für die Software-Entwicklung

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

### 4.3 UI & End-to-End Testing (Referenz: Osthues Insight Engine)

BDD ist nicht auf Backend-Logik beschränkt. Für Anwendungen mit grafischer Benutzeroberfläche spezifizieren wir Nutzerinteraktionen als Verhalten.

*Feature File:*
```gherkin
Scenario: Candidate Selection in Data Grid
    When the user selects the candidate "Max Mustermann" in the data grid
```

**Technische Umsetzung (Selenium Abstraktion):**
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

## 5. Architecture by Design: Ports & Adapters

Feature Files können genutzt werden, um architektonische Kapselung zu erzwingen.

### 5.1 Fallstudie: Kapselung von API-Clients (Referenz: AutoDNS Library)

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

**Technische Umsetzung (Library Test Wrapper):**
Ein CLI-Wrapper (`main.go`) ruft direkt die Library-Funktionen auf.

```go
// cmd/autodns-lib-test/main.go
func main() {
    // Ruft direkt die Library auf, ohne HTTP Server
    client := autodns.NewClient(...)
    client.Login()
}
```

**Konsequenz & Fazit:**
Der Test erzwingt eine **saubere Code-Architektur**. Spaghetti-Code ist unmöglich, da der API-Client als isoliertes Modul (`pkg/autodns`) vorliegen muss, um unabhängig vom Webserver getestet werden zu können. Das Feature-File fungiert hier als Architekt.

### 5.2 Fallstudie: Hexagonale Architektur (Referenz: PaperSink)

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

**Technische Umsetzung (Dependency Injection):**
Der Core definiert nur das Interface (`ports.DocumentRepository`). Der Adapter (`firestore.Repository`) implementiert dieses. Beim Testen können wir nun entscheiden, ob wir den echten Adapter oder einen Mock verwenden.

```go
// internal/core/ports/ports.go
type DocumentRepository interface {
    Save(ctx context.Context, doc domain.Document) error
}

// internal/adapter/firestore/repository.go
func (r *FirestoreRepository) Save(...) error { ... }
```

**Konsequenz & Fazit:**
Die Applikation wird **unabhängig von Technologien**. Wir können die Datenbank von Firestore zu Postgres wechseln, ohne eine Zeile im `core`-Code zu ändern, solange der neue Adapter denselben Port bedient. BDD-Tests validieren das Verhalten des Cores unabhängig vom verwendeten Adapter.

## 6. Strategien für externe Abhängigkeiten (Mocking & Infrastruktur)

Moderne Systeme interagieren mit komplexen Infrastrukturen. In unserer BDD-Methodik nutzen wir deterministische Mocks.

### 6.1 Deklaratives Mocking mit Mockoon (Referenz: DDNS Service)

HTTP-Abhängigkeiten werden über Mock-Server gesteuert, deren Konfiguration im Feature-File referenziert wird.

*Feature File:*
```gherkin
Scenario: A client update using specific API behavior
    Given the Mockoon server is running with "bdd/mockoon_environment.json"
```

**Technische Umsetzung (Container Control):**
Der Step startet einen Docker-Container mit der Spec-Config.

```python
subprocess.run(["docker", "run", ..., "mockoon/cli", "--data", config_file])
```

**Konsequenz & Fazit:**
Wir testen **Spec-First**. Da der Mock direkt aus der OpenAPI-Spezifikation des Fremdsystems generiert wird, validieren wir, dass unser Service konform zur offiziellen Schnittstellenbeschreibung ist, anstatt gegen handgeschriebene, potenziell falsche Mocks zu testen.

### 6.2 Infrastruktur-Mocking: PKI & DNS (Referenz: DDNS Service)

Sogar systemnahe Komponenten wie Verschlüsselung (TLS) können spezifiziert werden.

*Feature File:*
```gherkin
Scenario: Successful update with TLS 1.2
    Given the ddns-service is configured with:
      | key            | value                      |
      | custom-ca-cert | mock-server/pki/rootCA.crt |
```

**Technische Umsetzung (Envoy & Zertifikate):**
Wir nutzen einen Envoy Proxy mit Test-Zertifikaten.

```python
# Step: Starte Service mit dem Custom CA Zertifikat
# ./bin/service --custom-ca-cert=mock-server/pki/rootCA.crt
```

**Konsequenz & Fazit:**
Sicherheitsrelevante Features werden **testbar**. Wir verlassen uns nicht darauf, dass "TLS schon irgendwie geht", sondern weisen durch Tests nach, dass der Service z.B. unsichere Verbindungen (TLS 1.0) aktiv ablehnt oder korrekte Zertifikatsketten validiert.

### 6.3 AI-Accelerated Mocking: Ad-hoc System-Repliken

Durch den Einsatz von AI Agents können Nachbarsysteme **Ad-hoc** als Mocks generiert werden.

*Feature File:*
```gherkin
Scenario: Create a new board on Trello Mock
    Given a Trello Mock Server is listening on port 3000
```

**Technische Umsetzung (Dynamic Python Server):**
Der Agent generiert einen `http.server`, der *genau* die benötigten Endpoints implementiert.

**Konsequenz & Fazit:**
**Shift-LeftTesting**. Wir können Integrationstests schreiben, noch bevor das echte Nachbarsystem verfügbar oder lizenziert ist. Die Abhängigkeit von externen Teams entfällt.

## 7. Der iterative Prozess (Red/Green)

Die Entwicklung folgt einem strikten iterativen Prozess.

1.  **Red State:** Anforderung im Feature-File formulieren -> `behave` scheitert.
2.  **Implementation:** KI generiert Code (App + Steps).
3.  **Green State:** `make test` läuft durch.

## Schlusswort

Die Qualität des Software-Produkts korreliert direkt mit der Präzision der Feature-Files. Indem wir Infrastruktur, Daten und Architektur in die Spezifikation heben, schaffen wir Systeme, die durch KI deterministisch reproduzierbar sind.