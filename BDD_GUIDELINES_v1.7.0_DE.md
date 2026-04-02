# AI-Driven Behavior Driven Development: Praktische Richtlinien fuer spezifikationsgetriebene Software-Entwicklung

**Version: 1.7.0**

## Praeambel

Diese Richtlinien beschreiben einen pragmatischen BDD-Prozess fuer die Software-Entwicklung mit KI-Unterstuetzung.

Die zentrale Annahme lautet:

**Feature-Files in Gherkin sind die Single Source of Truth fuer die Fachlichkeit.**

Das bedeutet:

- Fachliche Anforderungen, erwartbares Verhalten und sichtbare Geschaeftsregeln werden im Feature-File beschrieben.
- Step-Code, Test-Hilfscode und Implementierung dienen dazu, dieses Verhalten auszufuehren und zu validieren.
- Versteckte fachliche Regeln im Glue Code sind zu vermeiden.

Nicht gemeint ist:

- dass jedes technische Detail im Feature-File stehen muss,
- dass Feature-Files Architekturdiagramme, Typsysteme oder Betriebsdokumentation ersetzen,
- oder dass ein gruener BDD-Test einen formalen Beweis fuer Korrektheit, Sicherheit oder Speichersicherheit darstellt.

BDD ist in diesem Dokument keine Ideologie, sondern ein Werkzeug zur Erhoehung von Klarheit, Rueckverfolgbarkeit und technischer Disziplin.

## 1. Grundprinzipien

### 1.1 Fachliche Single Source of Truth

Wenn es um Fachlichkeit geht, ist das Feature-File fuehrend.

Das umfasst insbesondere:

- erwartbares Verhalten von APIs, UIs, Jobs und Services,
- fachliche Eingabedaten und erwartete Resultate,
- fachliche Ableitungsregeln,
- Fehlerfaelle und Ablehnungsregeln,
- beobachtbare Seiteneffekte auf Nachbarsysteme.

Nicht ins Feature-File gehoeren technische Innereien ohne fachlichen Nutzen, etwa:

- konkrete Klassenhierarchien,
- private Hilfsmethoden,
- Framework-spezifische interne Flags,
- irrelevante Refactoring-Details.

### 1.2 Sichtbares Verhalten statt interner Vermutung

BDD spezifiziert das von aussen beobachtbare Verhalten eines Systems.

Tests sollen bevorzugt validieren:

- Rueckgabewerte,
- HTTP-Responses,
- erzeugte Dateien,
- persistierte Daten,
- Nachrichten in Queues,
- Logs mit fachlicher oder betrieblicher Relevanz,
- sichtbare UI-Zustaende.

Tests sollen nicht primaer bestaetigen:

- dass eine bestimmte private Methode aufgerufen wurde,
- dass eine bestimmte Implementierungsstrategie verwendet wurde,
- oder dass der Test seine eigene Hilfslogik erneut reproduziert.

### 1.3 Keine versteckte Fachlogik im Glue Code

Step-Implementierungen muessen moeglichst dumm sein.

Ihre Aufgabe ist:

- Eingaben aus dem Feature-File zu lesen,
- das System unter Test anzusteuern,
- Resultate aufzunehmen,
- Resultate gegen die Spezifikation zu vergleichen.

Ihre Aufgabe ist nicht:

- Fachlogik nachzubauen,
- fehlende fachliche Daten zu erraten,
- heimlich Default-Werte zu injizieren,
- fachliche Sonderfaelle zu kaschieren.

## 2. Datenexplizitheit

### 2.1 Alle fachlich relevanten Daten muessen sichtbar sein

Ein gutes BDD-Szenario ist fachlich vollstaendig genug, um ohne Blick in den Step-Code verstanden zu werden.

Wenn ein `Then`-Schritt einen konkreten Wert erwartet, dann muss dieser Wert entweder:

1. im `Given` explizit enthalten sein, oder
2. durch eine im Szenario klar erkennbare Geschaeftsregel ableitbar sein.

### 2.2 Requirement Gaps vermeiden

Ein Requirement Gap liegt vor, wenn ein erwarteter Wert im Szenario verlangt wird, seine Herkunft aber unsichtbar bleibt.

Schlechtes Beispiel:

```gherkin
Scenario: Map Order to Marketplace
  Given an order for item "X"
  When the mapping logic is applied
  Then the output must contain:
    | field | value       |
    | iban  | DE123456789 |
    | tax   | VAT_DE      |
```

Hier bleibt unklar, woher `DE123456789` und `VAT_DE` kommen.

Konsequenz:

- Die Implementierung oder der Step-Code wird den Wert mit hoher Wahrscheinlichkeit hardcodieren.
- Der Test bestaetigt dann keine allgemeine Logik, sondern nur einen statischen Textabgleich.

### 2.3 Anti-Hardcoding-Strategie

Um versteckte Konstanten aufzudecken, gelten drei Regeln:

- Vollstaendigkeit: Alle fachlich relevanten Quelldaten muessen sichtbar sein.
- Varianz: Fuer kritische Felder sollten mindestens zwei unterschiedliche Szenarien existieren.
- Ableitungsregel: Wenn Werte berechnet werden, muss die fachliche Regel erkennbar sein.

`Scenario Outline` ist hier oft das richtige Mittel.

### 2.4 Trennung von Stamm- und Bewegungsdaten

Bei komplexeren Domaenen sollten statische Konfigurationen und fallbezogene Daten getrennt werden.

Empfehlung:

- Stammdaten explizit als JSON oder Tabelle im `Given`.
- Bewegungsdaten separat als JSON, Tabelle oder referenziertes Artefakt.

So bleibt das Feature-File lesbar, ohne fachliche Vollstaendigkeit aufzugeben.

## 3. Komplexe Datenstrukturen

### 3.1 DocStrings fuer JSON und Payloads

Komplexe Daten gehoeren nicht in kryptische Hilfsobjekte im Step-Code, sondern sichtbar ins Szenario.

Beispiel:

```gherkin
Scenario: Upload a valid invoice document
  Given the client provides business metadata:
    """
    {
      "invoice_number": "INV-2026-001",
      "net_amount": 10050,
      "currency": "EUR"
    }
    """
```

Der Step-Code darf dieses JSON parsen und technisch an die Anwendung uebergeben. Er darf es aber nicht fachlich erweitern oder reparieren.

### 3.2 Transformationslogik sichtbar machen

Mapping-Logik zwischen Quell- und Zielsystemen ist haeufig reine Fachlogik. Sie sollte im Feature-File als Beispiel sichtbar sein.

Beispiel:

```gherkin
Scenario: Mapping custom fields from source to target
  Given a source order with custom fields:
    | source_code | value |
    | color-01    | blue  |
    | size-x      | 42    |
  When the mapping logic is applied
  Then the target structure should contain:
    | target_field   | value |
    | attributes.col | blue  |
    | attributes.sz  | 42    |
```

### 3.3 Artefakte statt Fantasiedaten

Wo sinnvoll, sollten echte oder realistische Artefakte verwendet werden:

- JSON-Dateien,
- XML-Payloads,
- Rechnungen,
- Log-Ausgaben,
- Beispielnachrichten,
- Mail-Messages,
- CSV-Dateien.

Das senkt das Risiko, dass nur eine kuenstliche Testwelt optimiert wird.

## 4. Testdesign

### 4.1 Das Verbot des Zirkelschlusses

Der Test darf die Fachlogik nicht selbst nachbauen.

Schlecht:

- Der Test berechnet im Python-Step denselben Bruttopreis wie die Anwendung.
- Der Test erzeugt intern dieselbe Mapping-Tabelle wie die Implementierung.

Gut:

- Der Test liefert Eingaben.
- Die Anwendung erzeugt ein Ergebnis.
- Der Test vergleicht das sichtbare Ergebnis gegen die Spezifikation.

### 4.2 Positive und negative Pfade

Fuer wichtige Fachfaelle sollen immer sowohl Erfolgs- als auch Fehlerpfade vorhanden sein.

Mindestens abzudecken sind:

- Happy Path,
- Validierungsfehler,
- fachliche Ablehnungen,
- technische Fehler mit fachlicher Auswirkung,
- relevante Randfaelle.

### 4.3 Silent Failures explizit pruefen

Ein Test darf sich nicht auf Statuscodes oder Erfolgsmeldungen allein verlassen.

Wenn das System Erfolg signalisiert, muss bei kritischen Prozessen auch der Zielzustand validiert werden, zum Beispiel:

- Datensatz wurde wirklich gespeichert,
- Nachricht wurde wirklich publiziert,
- Objekt wurde wirklich erzeugt,
- Mail wurde wirklich abgelegt,
- UI zeigt nicht nur Erfolg, sondern reflektiert den neuen Zustand.

### 4.4 Eventual Consistency sauber behandeln

In verteilten Systemen darf nicht vorschnell mit einem einzigen `assert` gearbeitet werden.

Stattdessen gilt:

- Polling mit klar definiertem Timeout,
- nachvollziehbare Fehlermeldungen,
- keine endlosen Sleeps ohne Begruendung,
- keine Flakiness als akzeptierter Normalzustand.

## 5. Step-Implementierungen

### 5.1 Aufgaben der Steps

Step-Dateien sind Adapter zwischen Spezifikation und System.

Sie sollen:

- Daten aus Gherkin lesen,
- das System starten oder ansteuern,
- Mocks konfigurieren,
- Ergebnisse speichern,
- standardisierte Assertions ausfuehren.

Sie sollen nicht:

- Fachlogik enthalten,
- Testdaten heimlich mutieren,
- implizite Defaults nachreichen,
- komplexe Berechnungen verstecken.

### 5.2 Modularisierung

Mit steigender Komplexitaet muessen Steps sauber geschnitten werden.

Empfohlene Struktur:

```text
bdd/steps/
├── ingress_steps.py
├── logic_steps.py
├── persistence_steps.py
├── ui_steps.py
└── cloud_steps.py
```

Jede Step-Datei sollte einen klaren Verantwortungsbereich haben.

### 5.3 Test-Hilfscode ist Infrastruktur, nicht Wahrheit

Helper, Fixtures und Mocks sind notwendig, aber sie sind nicht die fachliche Quelle der Wahrheit.

Wenn ein Konflikt zwischen Feature-File und Test-Hilfscode besteht, ist das Feature-File fuer die Fachlichkeit massgeblich.

## 6. Isolation und Laufzeitumgebung

### 6.1 Isolierte Testumgebung

BDD-Tests sollen in einer isolierten Laufzeitumgebung laufen.

Ziele:

- reproduzierbare Abhaengigkeiten,
- keine Vermischung mit lokaler Entwicklerumgebung,
- kontrollierte Versionen,
- klare Startbedingungen.

Je nach Stack kann das bedeuten:

- `.venv`,
- Container,
- dedizierte Testdatenbank,
- separater Browser-Kontext,
- isolierte Queue oder Bucket.

### 6.2 Housekeeping vor Teststart

Vor Testbeginn muss die Umgebung sauber sein.

Beispiele:

- keine alten Container,
- keine Ghost-Prozesse auf Testports,
- keine alten Sessions oder Browser-Zustaende,
- keine verunreinigten Temp-Verzeichnisse,
- definierte Testdatenbasis.

## 7. Externe Abhaengigkeiten

### 7.1 Deterministische Mocks statt unkontrollierter Live-Abhaengigkeiten

Externe Systeme sollen fuer die meisten Tests durch kontrollierte Mocks ersetzt werden.

Geeignet sind unter anderem:

- HTTP-Mock-Server,
- Queue-Fakes,
- Test-Datenbanken,
- Filesystem-Sandboxes,
- lokale SMTP-, IMAP- oder DNS-Testsysteme.

Live-Systeme haben ihren Platz eher in wenigen, gezielten Integrations- oder Smoke-Tests.

### 7.2 Mocks muessen Verhalten simulieren, nicht Wunschdenken

Ein Mock ist nur dann sinnvoll, wenn er fuer den geprueften Fall relevantes Verhalten realistisch genug abbildet.

Beispiele:

- HTTP 429 mit Retry,
- Timeouts,
- 403 und 500 Fehler,
- verzogener Start eines Dienstes,
- partielle Daten,
- idempotente Wiederholungen.

## 8. Architektur und BDD

### 8.1 BDD soll gute Schnittstellen foerdern

BDD fuehrt oft natuerlich zu besserer Architektur, weil testbare Systeme explizite Schnittstellen brauchen.

Typische positive Effekte:

- bessere Trennung von Core und Infrastruktur,
- testbare Adapter,
- klarere Eingangs- und Ausgangsmodelle,
- weniger versteckte Seiteneffekte.

### 8.2 BDD ersetzt keine Architekturarbeit

BDD hilft dabei, Architektur zu schaerfen. Es ersetzt aber nicht:

- Architekturentscheidungen,
- Lasttests,
- Security-Reviews,
- statische Analyse,
- Typpruefung,
- formale Verifikation,
- Code-Reviews.

Ein gruener BDD-Test bedeutet nur:

- Das getestete Verhalten funktioniert fuer die getesteten Faelle.

Nicht mehr und nicht weniger.

## 9. Systemnahe Sprachen und Speicherfehler

BDD kann auch bei C, C++, Rust oder anderen systemnahen Komponenten nuetzlich sein.

Praktische Einsatzfaelle:

- API-Verhalten kleiner nativer Bibliotheken pruefen,
- Fehlerpfade reproduzierbar machen,
- Abstuerze in bekannten Szenarien sichtbar machen,
- Integrationsverhalten gegen das Host-System absichern.

Wichtig ist aber:

- Ein fehlender Crash ist kein Beweis fuer Speichersicherheit.
- Ein erfolgreicher `ctypes`-Test ersetzt weder Sanitizer noch Valgrind noch Fuzzing.
- BDD kann hier ergaenzen, aber nicht formale oder spezialisierte Werkzeuge ersetzen.

## 10. UI-Testing

### 10.1 Benutzerintention testen

UI-Szenarien sollen Benutzerintention beschreiben, nicht DOM-Interna.

Beispiel:

```gherkin
Scenario: Candidate selection in data grid
  When the user selects the candidate "Max Mustermann" in the data grid
```

Der Step-Code darf die technische Selektion kapseln. Das Feature-File beschreibt die Absicht.

### 10.2 Keine fragile Browser-Manipulation

Bevorzugt werden echte Benutzerinteraktionen oder realistische Simulationen:

- tippen,
- klicken,
- fokussieren,
- waehlen,
- absenden.

Direktes Setzen von Werten ohne relevante Events ist nur ein Fallback und muss bewusst erfolgen.

### 10.3 Browser-Isolation

UI-Tests sollen in isolierten Browser-Kontexten laufen, um Cache-, Cookie- und Session-Leaks zu vermeiden.

## 11. Iterativer Prozess

Der Entwicklungszyklus bleibt einfach:

1. Fachliches Verhalten im Feature-File beschreiben.
2. Test scheitert.
3. Implementierung und Step-Code ergaenzen.
4. Test wird gruen.
5. Refactoring ohne Aenderung der Fachlichkeit.

Entscheidend ist:

- erst Verhalten klar machen,
- dann implementieren,
- danach technisch aufraeumen.

## 12. Qualitaetskriterien fuer gute Feature-Files

Ein gutes Feature-File ist:

- fachlich klar,
- ohne versteckte Regeln lesbar,
- datenexplizit,
- nicht redundant,
- nicht technisch ueberladen,
- robust gegen triviales Hardcoding,
- relevant fuer das beobachtbare Verhalten.

Ein schlechtes Feature-File ist:

- voller magischer Werte,
- fachlich unvollstaendig,
- nur mit Blick in den Glue Code verstaendlich,
- technisch verraetselt,
- so allgemein, dass es nichts Konkretes absichert,
- oder so detailverliebt, dass es Refactoring unnoetig erschwert.

## 13. Spec-Audit: Verifikation der Implementierungstreue

### 13.1 Das Problem

LLM-generierter Step-Code und Produktivcode koennen eine BDD-Suite formal zum Bestehen bringen, ohne die Spezifikation ehrlich zu erfuellen. Das ist kein Randfall, sondern ein erwartbares Verhalten bei KI-gestuetzter Implementierung.

Typische Muster:

- Das System meldet Erfolg, hat aber intern nichts getan (Stub mit Statuscode).
- Test und Implementierung bestätigen sich gegenseitig durch identische Hardcoding-Werte, ohne dass eine echte Geschaeftsregel existiert.
- Step-Code injiziert fachliche Daten, die im Szenario nicht sichtbar sind, und verzerrt damit die Testrealitaet.

Ein gruener Testlauf allein ist deshalb kein hinreichender Nachweis fuer Implementierungstreue. Er muss durch eine unabhaengige Pruefung ergaenzt werden.

### 13.2 Drei Pruefmuster

Die folgenden drei Pruefungen operationalisieren bestehende Prinzipien dieses Dokuments. Sie koennen systematisch gegen jedes Szenario angewendet werden.

#### Pruefung 1: Persistence-Validierung (operationalisiert 4.3)

Fuer jedes Szenario mit einer schreibenden Operation (POST, PUT, DELETE, Datei erzeugen, Nachricht senden):

> Existiert ein nachgelagerter Pruefschritt, der den Zielzustand ueber einen zweiten, unabhaengigen Kanal validiert?

Ein unabhaengiger Kanal ist zum Beispiel:

- eine direkte Datenbankabfrage,
- das Lesen einer erzeugten Datei,
- das Abfragen einer Queue oder eines Event-Logs,
- ein separater GET-Request, der die geschriebenen Daten zurueckliefert.

Die API-Response der schreibenden Operation selbst ist kein unabhaengiger Kanal. Sie ist die Selbstauskunft des Systems und damit nicht ausreichend.

**Finding**, wenn: das Szenario nur den Statuscode oder die Response der schreibenden Operation prueft, ohne den Zielzustand unabhaengig zu verifizieren.

#### Pruefung 2: Herkunftsanalyse fuer Then-Werte (operationalisiert 2.2)

Fuer jeden konkreten Wert in einem `Then`-Schritt:

> Ist dieser Wert entweder (a) woertlich in einem `Given` oder `When` des Szenarios enthalten, oder (b) durch eine im Szenario erkennbare Geschaeftsregel aus den sichtbaren Daten ableitbar?

Beispiel fuer ein Finding:

```gherkin
Given current harvest volume is 1500 kg
When the prediction is requested
Then yieldPrediction must be 19662
```

Der Wert 19662 erscheint weder in den Eingaben noch ist eine Ableitungsregel sichtbar. Das eroeffnet die Moeglichkeit, dass Implementierung und Test denselben hardcodierten Wert verwenden, ohne dass eine reale Berechnung stattfindet.

Beispiel ohne Finding:

```gherkin
Given net amount is 100 EUR and tax rate is 19%
When the invoice is calculated
Then gross amount must be 119 EUR
```

119 = 100 * 1.19. Die Ableitungsregel ist im Szenario erkennbar.

**Finding**, wenn: ein erwarteter Wert weder explizit in den Eingaben steht noch aus sichtbaren Daten und einer benannten Regel ableitbar ist.

#### Pruefung 3: Daten-Symmetrie zwischen Szenario und Step-Code (operationalisiert 1.3)

Fuer jeden `Given`-Step, der Testdaten vorbereitet:

> Verwendet der Step-Code ausschliesslich Daten, die im Szenario sichtbar sind, oder fuegt er eigene fachliche Werte hinzu?

Beispiel fuer ein Finding:

```gherkin
Given climate data exists for cultivation zone 303
```

Der Step-Code fuegt `calendar_week=41, light_j=1200.5, temperature_day=20.2` in die Datenbank ein. Keiner dieser Werte ist im Szenario sichtbar. Wenn ein spaeterer `Then`-Schritt gegen diese Werte prueft, ist die Pruefung nicht nachvollziehbar.

Technische Infrastruktur-Daten (Fremdschluessel, IDs fuer referenzielle Integritaet, Datenbankverbindungen) sind von dieser Pruefung ausgenommen. Sie sind keine fachlichen Daten.

**Finding**, wenn: der Step-Code fachliche Werte injiziert, die im Szenario nicht vorkommen und die spaeter fuer Assertions relevant werden koennten.

### 13.3 Durchfuehrung

Das Spec-Audit wird als separater Pruefschritt nach der Implementierung durchgefuehrt, nicht als Teil des regulaeren Testlaufs.

Empfohlener Ablauf:

1. Implementierendes LLM schreibt Produktivcode und Step-Code.
2. Die BDD-Tests laufen gruen.
3. Ein unabhaengiger Audit-Agent prueft die drei Muster gegen alle Szenarien.
4. Der Mensch bewertet die Findings und entscheidet ueber Korrekturbedarf.

Zwei Regeln fuer den Audit-Agent:

**Rollentrennung.** Der Audit-Agent soll nicht derselbe Agent sein, der die Implementierung erstellt hat. Nicht weil ein LLM technisch nicht beides kann, sondern weil die Unabhaengigkeit die Erkenntnisqualitaet erhoeht. Wer eigenen Code reviewt, rationalisiert.

**Kein Produktivcode.** Der Audit-Agent soll bevorzugt nur Feature-Files und Step-Code lesen, nicht den Produktivcode. Die Pruefung stellt die Frage: Validiert der Step-Code das Verhalten ehrlich? Wenn der Audit-Agent den Produktivcode liest, besteht das Risiko, dass er die Implementierung als korrekt rationalisiert, statt die Luecke zwischen Spezifikation und Verifikation zu erkennen.

### 13.4 Einordnung

Ein Spec-Audit ersetzt weder Code-Reviews noch manuelle Tests. Es ist ein strukturierter Pruefschritt, der gezielt die drei haeufigsten Ehrlichkeitsluecken in LLM-generiertem Step-Code adressiert.

Nicht jedes Finding erfordert eine Korrektur. Manche Szenarien testen bewusst nur den Statuscode (etwa fuer reine Validierungs-Ablehnungen). Manche Given-Steps muessen zwangslaeufig Testdaten erzeugen, die nicht im Szenario stehen. Die Entscheidung ueber die Relevanz eines Findings liegt beim Menschen.

## Schlusswort

Diese Richtlinien sollen keine Dogmen erzeugen, sondern bessere Entwicklungspraxis.

Der Kern bleibt:

- **Feature-Files sind die Single Source of Truth fuer die Fachlichkeit.**
- Glue Code und Implementierung haben dieser Fachlichkeit zu dienen.
- Gute BDD-Praxis schafft Klarheit, reduziert versteckte Annahmen und verbessert die Testbarkeit.
- BDD ist ein starkes Werkzeug, aber kein Ersatz fuer professionelles Engineering ausserhalb des getesteten Verhaltens.
