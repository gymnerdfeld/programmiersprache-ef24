# 2 Taschenrechner

## 2.1 Einfache Rechnungen auswerten

In einem ersten Schritt geht es darum, eine verschachtelte Rechnung zu berechnen.

Um überhaupt etwas berechnen zu können, brauchen wir eine gewisse Anzahl von nützlichen Operation wie Plus, Minus und so weiter.  Wir schreiben dazu Funktionen in Python und speichern sie unter dem gewünschten Symbol in einem `dict` ab.

```py
def add(a, b):
    return a + b

...

operators = {
    '+': add,
    '-': sub,
    '*': mult,
    ...
}
```

In der Analogie zum Taschenrechner entsprechen diese _eingebauten Funktionen_ den einzelnen Tasten auf dem Rechner.

Bei der Berechnung einer verschachtelten Rechnung können zwei Fälle auftreten:
1. Eine Zahl kann direkt wieder zurück gegeben werden.
2. Bei einer Rechnung sind mehrere Schritte nötig:
     * Funktion für den Operator in den `operators` nachschlagen.
     * Alle Argumente evaluieren, denn vielleicht ist da ja noch eine Rechnung mit dabei.  Hier ruft sich `evaluate` selber &ndash; also rekursiv &ndash; auf.
     * Funktion mit den berechneten Werte für die Argumenten aufrufen, und das Resultat zurück geben.

```py
def evaluate(expr):
    match expr:
        # Einfache Werte
        case int(num) | float(num):
            return num
        # Operationen ausführen
        case [operator, *args]:
            function = operators[operator]
            args = [evaluate(arg) for arg in args]
            return function(*args)
        # Unbekannter Ausdruck
        case _:
            raise ValueError("Unbekannter Ausdruck")
```

## 2.2 Konstanten

Ein Taschenrechner hat oft auch Tasten für viel verwendete Konstanten wie $\pi$.  Die Tasten für Konstanten und Operationen unterscheiden sich dabei nicht.  Auch in Python werden Funktionen und Werte am selben Ort abgespeichert.

Um das zu verdeutlichen, können unsere `operators` zu `operators_and_constants` umbenennen.

```python
import math
import random

operators_and_constants = {
    "+": add,
    "-": sub,
    "*": mult,
    "/": div,
    "expt": pow,
    "sin": math.sin,
    "cos": math.cos,
    "pi": math.pi,
    "e": math.e,
    "random": random.random,
}
```

Den `evaluate`-Code passen wir entsprechend an, so dass einzelne Namen wie `+`, `sin` oder `pi` in den oben definierten `operators_and_constants` nachgeschlagen werden.

```python
def evaluate(expr):
    match expr:
        case int(number) | float(number):
            return number
        case str(name):
            return operators_and_constants[name]
        case [operator, *args]:
            function = evaluate(operator)
            args = [evaluate(arg) for arg in args]
            return function(*args)
        case _:
            raise ValueError("Unbekannter Ausdruck")
```

Dadurch, dass wir einen separaten Case für das Nachschlagen von Namen machen, können wir später unseren Code einfacher erweitern.

## 2.3 Variablen

Selbst bei einfachen Taschenrechnern können Werte zwischengespeichert werden. Darum möchten wir beliebige Werte unter beliebigen Namen abspeichern können.

Die erste Frage, die sich stellt, lautet: Wo speichern wir die Variablen ab? In einem separaten `dict` oder zusammen mit den Operatoren und Konstanten in `operators_and_constants`?

Schauen wir uns einmal an wie dies in Python funktioniert:

```py
>>> ausdrucken = print
>>> ausdrucken("hallo")
hallo
>>> print = 5
>>> ausdrucken(print)
5
```
Die Funktion `print` kann in der Variablen `ausdrucken` abgespeichert werden, und dann wieder als Funktion aufgerufen werden.  Und der Name der Funktion `print` kann als Variablennamen verwendet werden (auch wenn das vielleicht nicht sehr schlau scheint).  Python verwendet also ein und denselben Ort um Variablen _und_ Funktionen abzuspeichern.  Wir wollen das ähnlich handhaben, und machen darum keinen Unterschied zwischen Operatoren, Konstanten oder durch den oder die Benutzer:in definierte Variablen.  Dazu benennen wir `operators_and_constants` zu `operators_constants_and_variables` um. Gut, dass wir diesen `dict` and nur ganz wenigen Stellen verwenden.  (Wir finden dann schon noch einen besseren Namen, versprochen!)

Zweitens stellt sich die Frage nach einer sinnvollen Syntax für die Definition von Variablen. Wir haben uns für das Schlüsselwort `sto` geeinigt, wie wir das von Taschenrechnern zum Abspeichern von Werten (engl. _store_) her kennen.  Das Schlüsselwort wird gefolgt vom Namen der Variablen und vom Wert, der abgespeichert werden soll.

Zum Beispiel:
```scheme
> (sto x 9)
9
> (+ x 2)
11
```

Damit das Ganze funktioniert, muss die Funktion `evaluate` erweitert werden:
```py
def evaluate(expr):
    match expr:
        # Einfache Werte
        ...
        case str(name):
            return operators_constants_and_variables [name]

        # Spezialkonstrukte
        case ["sto", name, value]:
            value = evaluate(value)
            operators_constants_and_variables [name] = value
            return value
        ...
```

Wenn also anstelle einer Zahl ein Name kommt, schlagen wir den in den `operators_constants_and_variables` nach, und geben den gefundenen Wert zurück.

Das Abspeichern einer Variablen muss ein Spezialkonstrukt sein, denn der Name der Variablen existiert zu diesem Zeitpunkt noch gar nicht.  Wenn einen neue Variable definiert wird, muss zuerst der Wert berechnet werden, der abgespeichert werden soll. Erst danach kann der berechnete Wert unter dem angegebenen Namen in `operators_constants_and_variables` abgespeichert werden.

Jetzt können wir sogar Resultate von Rechnungen abspeichern:

```scheme
> (sto x (+ 2 3))
> (sto y (* x x))
> y
25
```