# Tutorial: Eine eigene Programmiersprache erstellen

In diesem Tutorial entwickeln wir Schritt für Schritt unsere eigene Programmiersprache.  Die resultierende Programmiersprache wird im Vergleich zu einer "richtigen" Programmiersprachen wie Python vereinfacht sein.  So verwenden wir eine sehr einfache, aber praktische Syntax, und beschränken uns &ndash; zumindest in der ersten Version &ndash; auf Zahlen als Datentypen.  Bei den Funktionen jedoch, dem wichtigsten Werkzeug zur Abstraktion in praktisch allen Programmiersprachen, machen wir keine Kompromisse.

## Inhalt
* [Übersicht](#übersicht)
* [Begriffe](#begriffe)
* [Referenzen](#referenzen)
* [1 Basis](1-basics.md)
   * [1.1 Syntax](1-basics.md#11-syntax)
   * [1.2 Interne Darstellung eines Programms](1-basics.md#12-interne-darstellung-eines-programms)
   * [1.3 Phasen der Ausführung](1-basics.md#13-phasen-der-ausführung)
        * [1.3.1 Tokenize-Phase](1-basics.md#131-tokenize-phase)
        * [1.3.2 Parse-Phase](1-basics.md#132-parse-phase)
        * [1.3.3 Evaluate-Phase](1-basics.md#133-evaluate-phase)
   <!-- * Erweiterte Phasen (optional) -->
* [2 Taschenrechner](2-calculator.md)
    * [2.1 Einfache Rechnungen auswerten](2-calculator.md#21-einfache-rechnungen-auswerten)
    * [2.2 Konstanten](2-calculator.md#22-konstanten)
    * [2.3 Variablen](2-calculator.md#23-variablen)
* [3 Programmiersprache](3-programming_language.md)
    * [3.1 Funktionen, erste Version](3-programming_language.md#31-funktionen-erste-version)
    * [3.2 Funktionen mit Environments](3-programming_language.md#32-funktionen-mit-environments)
    * [3.3 Funktionen nutzen (Blöcke und Library)](3-programming_language.md#33-funktionen-nutzen-blöcke-und-library)

## Begriffe
* **Host-Programmiersprache**: Die Programmiersprache, welche benutzt wurde, um eine Programmiersprache zu programmieren.  Bei uns ist das Python, bei Python ist es C.
* **Interpreter**: Das Programm, welches den in unserer Programmiersprache geschriebenen Code ausführt.
* **Tokenize**: Erste Phase bei der Ausführung eines Programms. Der Text mit dem Code wird zuerst in logische Blöcke aufgeteilt.  Zum Beispiel `"(+ 1.1 5.5)"` in `"("`, `"+"`, `1.1`, `5.5` und `")"`.
* **Parse**: Zweite Phase bei der Ausführung eines Programms. Das Übersetzen der Liste der Tokens in die _interne Darstellung_.
* **Interne Darstellung**: Interne Darstellung eines Programms, oft in einer Baum-ähnlichen Struktur.  Bei uns wird ein Programm mit verschachtelten Listen, Strings und Zahlen dargestellt.
* **Evaluate**: Dritte Phase bei der Ausführung eines Programms. Die interne Darstellung Schritt für Schritt ausführen, um am Schluss zu einem Resultat zu gelangen.
* **Schlüsselwort**: Wort, welches in einer Programmiersprache eine spezielle Bedeutung hat, und darum zum Beispiel nicht als Variablen- oder Funktionsnamen verwendet werden darf.  In unserer Sprache beispielsweise `sto`, oder `def` in Python.
* **Eingebaute Funktion**: Eine Funktion, welche in unserer Programmiersprache benutzt werden kann, aber in der Host-Programmiersprache programmiert wurde. Zum Beispiel `add` für die Addition zweier Zahlen.
* **Library-Funktion**: Eine Funktion, welche in unserer Programmiersprache benutzt werden kann und auch in unserer Programmiersprache programmiert wurde.  Die Library-Funktionen werden vor der Ausführung eines Programms geladen.
* **Lokale Variablen**: Variablen, welche nur innerhalb einer Funktion existieren.  Also alle Argumente der Funktion und auch alle Variablen, welche innerhalb der Funktion definiert wurden.
* **Environment**: Ort um Werte wie Variablen und Funktionen abzuspeichern.  Das Environment ändert sich, und ist beispielsweise innerhalb einer Funktion anders als ausserhalb.  Für Environments verwenden wir Pythons `ChainMap`-Datenstruktur.
* **Rekursion**: Funktionen die sich selber aufrufen. Zum Beispiel eine Funktion welche die Fakultät einer Zahl berechnet.






