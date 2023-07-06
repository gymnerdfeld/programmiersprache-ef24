# Auftrag zur rekursiven Fakultätsfunktion

In der aktuelle Version unserer Programmiersprache können Funktionen programmiert werden.  

Zum Beispiel kann man nun die Wurzelfunktion `sqrt` direkt in unserer Sprache umsetzen:

```scm
(var sqrt (fn (x) (expt x 0.5)))

(sqrt 4)  ;; -> 2.0
```

**Auftrag:** Teste deine Spreche mit einer selbst geschriebenen Funktion.

Nun wollen wir mit unserer Sprache eine Funktion programmieren, welche die Fakultät berechnet.

In Python kann die Fakultät folgendermassen rekursiv definiert werden:
```py
def fact(n):
    if n == 0:
        return 1
    else:
        return n * fact(n-1)
    
print(fact(5))  # -> 120
```

## `if` und Vergleichsoperatoren

Aktuell fehlt dazu in unserer Sprache noch die `if`-Anweisung sowie der `==`-Vergleichsoperator.

**Auftrag:** Bau ein `if` und `==` in deine Sprache ein.

Als ersten Test könnte die folgende `iszero?`-Funktion dienen, welche überprüft, ob eine Zahl null ist.
```scm
(var iszero? (fn (a) (if () 1 0)))

(iszero? 15)   ;; -> 0
(iszero? 0)    ;; -> 1
```

**Auftrag:** Überprüfe, ob dein `if` und `==` wunschgemäss funktioniert.

## Rekursive Funktionen und `if`

Nun kann die Fakultätsfunktion definiert werden:
```scm
(var fact
    (fn (a) 
        (if 
            (== 0 a) 
            1
            (* a (fact (- a 1)))
        )
    )
)
```

Oder auf einer Zeile für praktisches copy-pasten:
```scm
(var fact (fn (a) (if (== 0 a) 1 (* a (fact (- a 1))))))
```

**Auftrag:** Teste die `fact`-Funktion
 
```scm
(fact 5)  ;; -> 120
```

Falls du den folgenden Fehler erhälst, bist du auf dem richtigen Weg.
```
Error: RecursionError('maximum recursion depth exceeded')
```

Offenbar hast du eine unendliche lange Berechnung gestartet. Was könnte der Grund dafür sein?

_Tipp:_ Studiere die [Zeile 78](#file-taschenrechner-py-L78) im Code unten.

**Auftrag:** Ändere deinen Code, so dass der Fehler nicht mehr auftritt.

(Ein Zusatztipp gibt es in der zweiten Ferienwoche)

## Zusatzaufgabe

Falls du die Lösung für den obigen Fehler gefunden hast, ist es an der Zeit, eine weiter rekursive Funktion in unserer Programmiersprache zu coden.

**Auftrag:** Schreib eine Funktion, welche die n-te Zahl der [Fibonacci-Folge](https://de.wikipedia.org/wiki/Fibonacci-Folge) berechnet.