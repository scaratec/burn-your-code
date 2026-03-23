# Changelog zu BDD Guidelines v1.6.0

## Ziel der Ueberarbeitung

Die Version 1.6.0 macht die Guidelines fachlich und methodisch belastbarer.

Sie behaelt den Kern bei:

- Feature-Files sind die Single Source of Truth fuer die Fachlichkeit.

Gleichzeitig entfernt sie Aussagen, die methodisch ueberzogen oder unserioes wirken.

## Wesentliche Aenderungen gegenueber v1.5.0

### 1. Single Source of Truth praezisiert

Die fruehere Fassung verwendete den Begriff sehr breit.

In v1.6.0 ist klarer formuliert:

- Single Source of Truth gilt fuer die Fachlichkeit.
- Nicht jedes technische Detail muss im Feature-File stehen.
- Feature-Files ersetzen keine Architektur-, Betriebs- oder Sicherheitsdokumentation.

### 2. Beweisrhetorik entfernt

Entfernt oder deutlich abgeschwaecht wurden Aussagen wie:

- mathematischer Beweis,
- Beweis von Memory Safety durch BDD,
- Beweis architektonischer Korrektheit,
- implizite Gleichsetzung von gruenen Tests mit technischer Wahrheit.

Stattdessen ist nun klarer benannt:

- gruene BDD-Tests zeigen nur, dass getestetes Verhalten fuer getestete Faelle funktioniert,
- spezialisierte Werkzeuge wie Sanitizer, Fuzzing, Lasttests, statische Analyse und Security-Reviews bleiben notwendig.

### 3. Glue Code methodisch geschaerft

Die neue Fassung betont staerker:

- Glue Code darf keine versteckte Fachlogik enthalten,
- Steps sollen Adapter zwischen Gherkin und System sein,
- Test-Hilfscode ist Infrastruktur, nicht fachliche Wahrheit.

### 4. Datenexplizitheit und Anti-Hardcoding beibehalten

Die starken Teile der alten Fassung wurden bewusst erhalten und gestrafft:

- sichtbare Herkunft fachlicher Werte,
- Requirement Gaps vermeiden,
- Varianz gegen Hardcoding,
- Trennung von Stamm- und Bewegungsdaten,
- sichtbare Transformationslogik.

### 5. Architektur-Abschnitt entideologisiert

Die alte Fassung stellte BDD stellenweise als Architekturtreiber mit nahezu zwingender Wirkung dar.

Die neue Fassung sagt stattdessen:

- BDD foerdert oft bessere Schnittstellen,
- BDD ersetzt aber keine Architekturarbeit,
- gute Architektur braucht weiterhin explizite technische Entscheidungen.

### 6. Systemnahe Entwicklung realistischer eingeordnet

Die neue Fassung erkennt den Nutzen von BDD fuer native Komponenten an, zieht aber eine klare Grenze:

- kein Crash ist kein Beweis fuer Speichersicherheit,
- `ctypes`-Tests koennen nuetzlich sein,
- sie ersetzen aber keine dafuer vorgesehenen Werkzeuge.

### 7. Ton und Anspruch professionalisiert

Version 1.6.0 ist insgesamt:

- weniger absolut,
- weniger missionarisch,
- weniger theoretisch ueberdehnt,
- dafuer klarer, nuchterner und glaubwuerdiger.

## Praktische Folge

Die Guidelines bleiben anspruchsvoll und disziplinierend, aber die Aussagen sind besser mit realer Engineering-Praxis vereinbar.

Das Ziel ist nicht weniger Ambition, sondern mehr fachliche und technische Seriositaet.
