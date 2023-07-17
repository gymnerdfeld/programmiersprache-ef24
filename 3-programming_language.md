# 3 Programmiersprache

## 3.1 Funktionen, erste Version

Jetzt wollen wir unseren "Rechner" zu einem programmierbaren Rechner erweitern.  Wir wollen also eigene Funktionen in unserer eigenen Sprache schreiben, welche wir danach aufrufen können.  In der ersten Version werden unsere Funktionen noch nicht ganz so funktionieren, wie wir das von den bekannten Programmiersprachen her gewohnt sind.

Bevor wir loslegen können, müssen wir uns Gedanken zur Syntax machen.  Mit `sto` haben wir bereits einen Weg gefunden, um etwas unter einem Namen abzuspeichern.  Wir brauchen also zusätzlich noch einen Weg, wie wir eine Funktion mit ihren Parametern schreiben wollen.  Dazu betrachten wir zuerst die Definition und das Ausführen von Funktionen in Python, um uns danach für unsere eigene Syntax zu entscheiden.

![](funktionen.png)

Als Schlüsselwort verwenden wir `phonk`, gefolgt von der Liste mit den Parametern und zuletzt dem Body der Funktion, also dem eigentlichen Code der ausgeführt werden soll.

Ein weiteres Beispiel könnte so aussehen:

```scheme
(sto square        ; <- Unter dem Namen `square` abspeichern
    (phonk (x)     ; <- Definition einer Funktion (ohne Namen) mit einem Parameter mit dem Namen `x`
        (* x x)    ; <- Body der Funktion
    )
)

(square 5)         ; <- Die oben definierte Funktion ausführen, mit 5 als Argument
```

Denselben Code auf jeweils einer Zeile:
```scheme
(sto square (phonk (x) (* x x)))
(square 5)
```

Der Code einer Funktion wird bei der Definition nicht ausgeführt, sondern abgespeichert.  Darum muss die Definition einer Funktion mit `phonk` ist ein Spezialkonstrukt unserer Sprache sein.  Der Code dazu ist sehr einfach.  Wir können einfach die Liste mit den Namen der Parameter und den Body der Funktion unverändert zurück geben.  Der _Body_ der Funktion ist der Code, welcher ausgeführt werden soll, wenn die Funktion aufgerufen wird.
```py
def evaluate(expr):
    match expr:
        ...
        # Spezialkonstrukte
            ...
        case ["phonk", params, body]:
            return ["phonk", params, body]
```


Beim Ausführen der Funktion wird es etwas komplizierter.  Am Anfang bleibt alles wie gehabt. Wir holen die Funktion aus den `operators_constants_and_variables`, welches wir mittlerweile zu `everything` umbenannt haben, und evaluieren alle Argumente.  Danach müssen wir unterscheiden, um was für eine Funktion es sich handelt:
 * Eine Funktion, welche in unserer Sprache geschrieben wurde
 * Eine in Python geschriebene _eingebaute Funktion_

Unsere eigenen Funktionen sind Listen aus dem Schlüsselwort `phonk`, den Namen der Parameter und dem Body der Funktion.  Alles andere ist dann (hoffentlich) eine in Python geschriebene Funktion:

```py
def evaluate(expr):
    match expr:
        ...
        # Funktionen
        case [operator, *args]:
            function = evaluate(operator)
            args = [evaluate(arg, env) for arg in args]

            match function:
                # "Eigene" Funktion
                case ["phonk", params, body]:
                    for i in range(len(params)):
                        value = args[i]
                        name = params[i]
                        everything[name] = value
                    return evaluate(body)

                # Python Funktion
                case _:
                    return func(*args)
```

Bei den eingebauten Python-Funktionen ganz unten ist alles wie bisher: Direkt aufrufen.

Bei unseren "eigenen" Funktionen sind zwei Schritte nötig:
1. Die übergebenen Werte (Argumente) müssen unter den in der Funktionsdefinition angegebenen Parameternamen abgespeichert werden.
2. Der Body wird evaluiert und das erhaltene Resultat zurück gegeben.

_Bemerkung:_ Bei den beiden Begriffe Parameter und Argumente einer Funktion droht Verwechslungsgefahr. Als Parameter bezeichnet man die Liste von Namen bei der _Definition_ einer Funktion.  Die konkreten Werte, welche dann beim _Aufruf_ einer Funktion übergeben werden, nennt man hingegen Argumente.  Sie zu verwechseln ist aber oft nicht weiter schlimm, denn meistens ist trotzdem klar, was gemeint ist. In der Python-Welt werden diese beiden Begriffe aber ziemlich konsistent wie beschrieben verwendet.


## 3.2 Funktionen mit Environments


<!-- Leakt Variablen

Beispiel, dass nicht funktioniert:
```scheme
(sto incr (phonk (a) (+ a 1)))
(sto a 10)
(sto b 1)
(+ (incr b) a)
```
Gibt 3 anstatt 12. -->


Mit obigen Version gibt es jedoch ein unschönes Problem:
```scheme
> (sto square (phonk (x) (* x x)))
[ ... ]
> (square 5)
25
> x
5
```
Nach dem Aufruf der Funktion `square` existiert plötzlich die Variable `x`.  Eventuell wurde durch den Aufruf von `square` eine bereits existierende Variable `x` überschrieben.  Dies weil es nur einen einzigen Ort gibt, an dem Variablen abgespeichert werden können: `everything`.

Die Erwartung ist aber, dass Variablen einer Funktion nur innerhalb dieser Funktion existieren.  So  ist es zum Beispiel in Python:
```py
>>> def square(x):
...     return x * x
...
>>> square(5)
25
>>> x
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'x' is not defined
```

Bei jedem Aufruf einer Funktion wollen wir also einen neuen Ort erstellen, an welchem die lokalen Variablen gespeichert werden können. Nach derm Ausführen der Funktion brauchen wir die erstellten lokalen Variablen nicht mehr. Es ist wie ein frisches Blatt Papier, auf welchem wir die Variablen der Funktion notieren.  Am Ende der Funktionsausführung zerknüllen wir das Papier, und schmeissen es weg.

Den neuen `dict` für die lokalen Variablen erstellen wir in einer Liste.  Zuvorderst in dieser Liste kommen die lokalen Variablen, und weiter hinten dann die globalen Variablen und eingebaute Funktionen.  Wenn wir den Wert für einen Namen suchen, gehen wir diese Liste von vorne nach hinten durch, und schauen, ob in den jeweiligen `dicts` etwas unter dem Namen abgespeichert ist.  Diese ganze Liste mit `dicts` nennen wir _Environment_.  Dieses Environment kann anders sein, je nach dem, wo wir uns im Code befinden.  Zum Beispiel haben wir innerhalb einer Funktion ein zusätzliches `dict` zuvorderst, in welchem wir die lokalen Variablen abspeichern.

Wir müssen unseren Code dazu an einigen Stellen umbauen.

Als erstes können wir unser dict `everything`, wo wir vorher alles mögliche drin gespeichert hatten, umbenennen. Wir nennen es neu `builtins`, da es jetzt nur noch die eingebauten Funktionen enthält. Da wir jetzt den Schritt weg von einem Taschenrechner zu einer Programmiersprache machen, brauchen wir neu nur noch das Wort _Funktionen_ für alle Operatoren.

```py
builtins = {
    "+", add,
    ...
}
```

Nun kreieren wir ein globales Environment, in welchen sich zuhinterst auch die eingebauten Funktionen `builtins` befinden:
```py
global_env = [{}, builtins]
```

Unser `evaluate` soll nun für den gleichen Code ein anderes Resultat produzieren, je nachdem in welcher Umgebung also Environment der Code ausgeführt wird. `evaluate` nimmt also nicht nur den Code unter dem Namen `expr` entgegen, sondern auch noch das Environment `env`. Falls kein `env` angegeben wird, nehmen wir an, dass der Code mit dem globalen Environment `global_env` ausgewertet werden soll.

```py
def evaluate(expr, env=global_env):
    match expr:
        # Einfache Werte
        case int(num) | float(num):
            return num`
    ...
```

Das Nachschlagen der Werte müssen wir nun den neuen Gegebenheiten anpassen. Unser _Environment_ ist neu eine Liste von `dicts`, welche wir von vorne nach hinten durchgehen. Finden wir unter dem gesuchten Namen `name` etwas, können wird diesen Wert zurück geben. Falls wir aber alles durchgehen, und bis am Schluss nicht fündig werden, geben wir eine Fehlermeldung aus.

```py
def evaluate(expr, env=global_env):
    match expr:
        ...

        # Spezialkonstrukte
        case str(name):
            # Variablen im Environment von vorne nach hinten
            # suchen
            for local_env in env:
                if name in local_env:
                    return local_env[name]

            # Nichts gefunden unter dem angegebenen Name: Error
            raise NameError(f"name '{name}' is not defined")
```

Und auch beim Abspeichern von Werten nehmen wir zwei kleine, aber wichtige Änderung vor. Wir speichern neu eine Variable immer im vordersten `dict` des Environments ab. Und beim Evaluieren des Wertes `value` geben wir neu immer das aktuelle Environment `env` mit.
```py
def evaluate(expr, env=global_env):
    match expr:
        ...

        case ["var", name, value]:
            value = evaluate(value, env)

            # Neue Variable im vordersten dict vom Environment
            # abspeichern
            local_env = env[0]
            local_env[name] = value
            return f"{name} stored: {value}"
        ...
```

Jetzt kommen wir zum wichtigsten Teil unserer Änderungen, dem Aufruf von Funktionen. Zuerst passen wir den Aufruf  von `evaluate` für die Funktion und die Argumente so an, dass wir das aktuelle Environment mitgeben.

```py
def evaluate(expr, env=global_env):
    match expr:
        ...
        # Funktionen aufrufen
        case [operator, *args]:
            function = evaluate(operator, env)
            args = [evaluate(arg, env) for arg in args]
            match function:
                case ["phonk", params, body]:   # Eigene Funktionen
                    # Neues dict für lokale Variablen erstellen
                    local_env = {}

                    # Argumente unter den Parameternamen im neuen dict
                    # abspeichern
                    for i in range(len(params)):
                        value = args[i]
                        name = params[i]
                        local_env[name] = value

                    # Neues Environment erstellen, mit den neuen
                    # lokalen Variablen zuvorderst
                    new_env = [local_env, *env]

                    # Body in neuem Environment ausführen / evaluieren
                    return evaluate(body, new_env)
                case _:                         # Eingebaute Funktionen (in Python geschrieben)
                    return function(*args)
```
Treffen wir nun auf eine Funktion, welche in unserer eigenen Programmiersprache geschrieben wurde, erstellen wir ein neues `dict` für die lokalen Variablen, und speichern dort die Werte (Argumente) unter den Korrekten Namen (Parameternamen) ab.

Mit dem neuen `dict` `local_env` und den `dicts` des "alten" Environments erstellen wir nun ein neues Environment und nennen es `new_env`. Und das ist jetzt das Environment, mit welchem wir den Body der Funktion auswerten.

## 3.3 Funktionen nutzen (Blöcke und Library)

In unserer Konsole können wir schrittweise Rechnungen ausführen, dabei Zwischenresultate unter eigenen Namen abspeichern. Innerhalb von Funktionen ist das momentan noch nicht möglich, da der Body einer Funktion nur einen einzige Anweisung sein kann. Anstatt die Definition von Funktionen anzupassen, führen wir eine neue `block`-Anweisung ein, welche wir dann an ganz verschiedenen Orten einsetzen können.

Alle Anweisung innerhalb einer `block`-Anweisung werden der Reihe nach ausgeführt, und am Ende das Resultat der letzten Anweisung zurück gegeben. Zum Beispiel die folgende Rechnung:

```scheme
(block
    (sto a 4)
    (sto b 3)
    (sto c2 (+ (* a a) (* b b)))
    (sqrt c2)
)
```

Den `block` können wir als Spezialkonstrukt implementieren:
```py
def evaluate(expr, env=global_env):
    match expr:
        ...

        # Spezialkonstrukte
        ...
        case ["block", *statements, last]:
            for statement in statements:
                evaluate(statement, env)
            return evaluate(last, env)
```

Und wir wollen unsere neue `block`-Anweisung anwenden. Unserer Programmiersprache unterstützt nun Funktionen, und so können wir häufig gebrauchte Funktionen auch in unserer eigenen Programmiersprache schreiben, und müssen dabei nur noch in Ausnahmefällen auf Python zurück greifen. Diese Funktionen (und auch Definitionen von Konstanten) sammeln wir dann in der Standardbibliothek (engl. _standard library_ oder kurz _library_):
```py
library = """
(block
    (var e 2.718281828459045)
    (var pi 3.141592653589793)
    (var sqrt (fn (x) (expt x 0.5)))
    (var > (fn (a b) (< b a)))
)
"""
```



Damit wir diese Funktionen in unseren Programmen auch verwenden können, müssen wir die `library` beim Starten unseres Interpreters laden, also ausführen:
```py
def repl():
    """Read-Eval-Print-Loop: Unsere Konsole

    User-Eingabe analysieren und evaluieren.
    """
    run(library)

    while True:
        ...
```
