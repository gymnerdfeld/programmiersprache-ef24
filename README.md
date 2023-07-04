# Eine eigene Programmiersprache

## Basis

Wir schreiben unsere eigene Programmiersprache in Python.  Dazu bestimmen wir zuerst wie unsere Sprache aussehen soll.

### Syntax

Unsere Sprache lehnt sich vom Aussehen her an eine der ältesten Programmiersprachen an, welche immer noch aktiv verwendet wird: LISP.

Jede Operation in unserer Sprache wird dabei in Klammern geschrieben, mit dem Namen der Operation als erstes, gefolgt von den Argumenten. Als Trennzeichen braucht es kein Komma sondern ein einfaches Leerzeichen genügt.

Beispiel:
```lisp
(+ 1 3)
```

Operationen können beliebig verschachtelt werden:
```lisp
(+ 1 (* (- 7 2 ) 4))
```

Die Syntax ist im Vergleich zu Python nicht sehr leserlich, aber sehr einfach, und dadurch gut geeignet für Experimente.

### Interne Darstellung eines Programms

Ein Programm wird normalerweise in eine Textdatei geschrieben, auch Source-Code genannt.  Wir können den Inhalt der Datei als String einlesen.  Dieser String wird dann in die _interne Darstellung_ übersetzt.  Da unsere Syntax sehr einfach ist, entspricht die interne Darstellung fast exakt dem ursprünglichen Source-Code.  Wir verwenden dazu Listen, Strings und Zahlen (`int` und `float`).

_Beispiel:_

Source-Code:
```lisp
(+ (- 5 4) (* (- 7 2 ) 4))
```

Interne Darstellung in Python:
```py
['+', ['-', 5, 4], ['*', ['-', 7, 2], 4]]
```

Die interne Darstellung kann man auch als "Baum" darstellen.  (Nun ja, irgendwie wachsen die Äste gegen unten ...)

```py
    ['+',   …   ,    …]
            🡓        🡓
    ['-', 5, 4]    ['*', …, 4]
                         🡓
                       ['-', 7, 2]
```
Wegen dieser Baum-ähnlichen Struktur wird die _interne Darstellung_ oft auch _Abstract Syntax Tree_ (kurz _AST_) genannt.

### Phasen der Ausführung

Um vom Source-Code zu einem ausgeführten Programm zu gelangen sind (mindestens) drei Schritte nötig.  Diese Schritte werden im Informatikjargon _Phasen_ genannt.

#### Tokenize-Phase

In der ersten Phase wird der (lange) String mit dem Source-Code in Teile aufgetrennt, welche logisch zusammengehören. Zum Beispiel gehören bei `2.18` alle vier Zeichen zur gleichen Zahl.  Aus dem String `2 18`  werden jedoch zwei Tokens: `2` und `18`.  Die logischen Einzelteile werden _Tokens_ genannt.  Und darum heisst diese erste Phase auch _tokenize_. 

Der Tokenizer-Code ist Dank eines Tricks sehr kurz:
```py
def tokenize(program):
    return program.replace("(", " ( ").replace(")", " ) ").split()
```

#### Parse-Phase

In der zweiten Phase wird die Liste mit Tokens in die interne Darstellung umgewandelt.  Die Phase wird `parse` genannt, und besteht bei uns aus zwei Teilen:

Einerseits wird mit Listen die Struktur des Programms wiedergeben:
```py
def parse(tokens):
    token = tokens.pop(0)
    if token == '(':
        lst = []
        while tokens[0] != ')':
            lst.append(parse(tokens))
        tokens.pop(0)
        return lst
    else:
        return parse_atom(token)
```
Der Code dazu ist zwar kurz, aber ziemlich schwer verständlich.  Wir vertrauen einfach mal darauf, dass er funktioniert.

Andererseits benutzten wir die Python-Funktionen `int` und `float` um zu versuchen, Strings mit Zahlen in Zahlen (`int` oder `float`) umzuwandeln:
```py
def parse_atom(token):
    try:
        token = int(token)
    except ValueError:
        try:
            token = float(token)
        except ValueError:
            pass
    return token
```

Bei Sprachen mit einer schönen Syntax ist die `parse`-Phase sehr komplex, und war lange ein zentrales Problem in der Informatikforschung.  Zum Beispiel musste bei Python der komplett `parse`-Code ersetzt werden, um die neue `match`-`case`-Syntax einführen zu können.

#### Evaluate-Phase
In der dritten und letzten Phase wird die interne Darstellung des Programms ausgewertet, oder auf Englisch _evaluated_.

Die Auswertung geschieht rekursiv.  

Was passiert zum Beispiel wenn die folgende Rechnung ausgeführt werden soll?
```lisp
(+ (- 5 4) (* (- 7 2 ) 4))
```

In den ersten zwei Phasen wird der Code in die interne Darstellung übersetzt:
```py
['+', ['-', 5, 4], ['*', ['-', 7, 2], 4]]
```

Jetzt können wir schrittweise den Code ausführen.  Zur besseren Übersicht verwenden wir hier die Baum-ähnliche Darstellung:

1. Äusserste Liste evaluieren:
```py
    ['+',   …   ,    …]           # Muss zuerst Argumente evaluieren
            🡓        🡓
    ['-', 5, 4]    ['*', …, 4]
                         🡓
                       ['-', 7, 2]
```

2. Erstes Argument (`['-', 5, 4]`) evaluieren:
```py
    ['+',   …   ,    …]
            🡓        🡓
            1      ['*', …, 4]
                         🡓
                       ['-', 7, 2]
```

3. Zweites Argument (`['*', ['-', 7, 2], 4]`) evaluieren:
```py
    ['+',   1   ,    …]
                     🡓
                   ['*', …, 4]    # Muss zuerst Argumente evaluieren
                         🡓
                       ['-', 7, 2]
```

4. Argument `['-', 7, 2]` evaluieren:
```py
    ['+',   1   ,    …]
                     🡓
                   ['*', …, 4] 
                         🡓
                         5
```
5. Jetzt kann man `['*', 5, 4]` evaluieren:
```py
    ['+',   1   ,    …]
                     🡓
                     20
```
6. Und erst jetzt die ursprüngliche Rechnung `['+', 1, 20]` evaluieren:
```py
    21
```
