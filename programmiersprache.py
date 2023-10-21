# ====================================== #
# Die ersten beiden Phasen der Auführung #
# ====================================== #
def tokenize(program):
    """Programmtext in die logischen Blöcke aufteilen, und Kommentare entfernen
    """
    # Kommentare entfernen
    zeilen_alt = program.split("\n")
    zeilen_neu = []

    for zeile in zeilen_alt:
        if ";" in zeile:
            # An welcher Position steht das erste Semikolon?
            zeilen_neu.append(zeile[:zeile.find(";")])
        else:
            zeilen_neu.append(zeile)

    # Zeilen wieder zusammensetzten
    program = "\n".join(zeilen_neu)
    
    return program.replace("(", " ( ").replace(")", " ) ").split()

def parse(tokens):
    """Liste der Tokens in die interne Darstellung übersetzen.
    """
    token = tokens.pop(0)
    if token == '(':
        lst = []
        while tokens[0] != ')':
            lst.append(parse(tokens))
        tokens.pop(0)
        return lst
    else:
        return parse_atom(token)

def parse_atom(token):
    """Tokens, welche keine Klammern sind, wenn möglich umwandeln.
    """
    # Token scheint eine Zahl zu sein (hoffentlich)
    if token[0] in "+-.0123456789" and token != "+" and token != "-":
        if "." in token:
            return float(token)
        else:
            return int(token)
    else:
        return token

# ===================== #
# Eingebaute Funktionen #
# ===================== #
def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mult(a, b):
    return a * b

def div(a, b):
    return a / b

def div_int(a, b):
    return a // b

def expt(a, b):
    return a ** b

def less_than(a, b):
    return a < b

def block(*args):
    if len(args) == 0:
        return None
    else:
        return args[-1]

def dict_new():
    return {}

def dict_in(d, key):
    return key in d

def dict_add(d, key, val):
    d[key] = val
    return val

def dict_get(d, key):
    return d[key]

import math
import random

# Dict mit den eingebaute Funktionen
builtins = {
    # Die wichtigsten mathematischen Operationen
    "+": add,
    "-": sub,
    "*": mult,
    "/": div,
    "//": div_int,
    "expt": expt,   # "hoch"
    "sin": math.sin,
    "random": random.random,

    # Vergleichsoperator
    "<": less_than,

    # Mehrere Ausdrücke nacheinander ausführen
    "block": block,

    # Pythons True und False
    "True": True,
    "False": False,

    # Support für dicts
    "dict-new": dict_new,
    "dict-in": dict_in,
    "dict-add": dict_add,
    "dict-get": dict_get,
}

# =============================================== #
# Library (in unserer Sprache geschriebener Code) #
# =============================================== #
library = """
(block
    ;;;;;;;;;;;; Weitere Vergleichsfunktionen ;;;;;;;;;;;;;;;;;;
    (sto > (phonk (a b) (< b a)))
    (sto >= (phonk (a b) (if (< a b) False True)))
    (sto not (phonk (a) (if a False True)))
    (sto <= (phonk (a b) (not (> a b)) ))

    ;;;;;;;;;;;; Mathematische Konstanten ;;;;;;;;;;;;;;;;;;
    (sto pi 3.141592653589793)
    (sto e 2.718281828459045)    ; Eulersche Zahl

    ;;;;;;;;;;;; Mathematische Funktionen ;;;;;;;;;;;;;;;;;;
    ; Cosinus
    (sto cos (phonk (x)
        (sin (+ x (/ pi 2)))
    ))

    ; Fakultät
    (sto fact (phonk (n)
        (if (< n 2)
            1
            (* n (fact (- n 1)))
        )
    ))

    ; Betrag
    (sto abs (phonk (x)
        (if (< x 0)
            (- 0 x)
            x
        )
    ))

    ; Fibonacci-Zahlen, rekursiv (langsam) implementiert
    (sto fib (phonk (n)
        (if (< n 2)
            n
            (+ (fib (- n 1)) (fib (- n 2))))
    ))

    ; Quadratwurzel
    (sto sqrt (phonk (x) (block
        (sto sqrt-iter (phonk (guess)
            (if (good-enough? guess)
                guess
                (sqrt-iter (improve guess))
            )
        ))
        (sto good-enough? (phonk (guess)
            (< (abs (- (* guess guess) x)) 0.001)
        ))
        (sto improve (phonk (guess)
            (average guess (/ x guess))
        ))
        (sto average (phonk (x y)
            (/ (+ x y) 2)
        ))
        (sqrt-iter 1)
    )))

    ;;;;;;;;;;;; Cached "decorator" ;;;;;;;;;;;;;;;;;;
    (sto cached (phonk (func) (block
        (sto cache (dict-new))
        (sto new_func (phonk (x)
            (if (dict-in cache x)
                (dict-get cache x)
                (block
                    (sto res (func x))
                    (dict-add cache x res)
                    res
                )
        )))
        new_func
    )))

    ; Cached "decorator" auf fib anwenden
    (sto fib (cached fib))

    ;;;;;;;;;;;; Closure Experimente ;;;;;;;;;;;;;;;;;;
    (sto make_adder (phonk (x) (block
        (sto adder (phonk (y)
            (+ x y)
        ))
        adder
    )))

    (sto plus5 (make_adder 5))
)
"""

# Globales Environment
global_env = [{}, builtins]

# =============================================== #
# Dritte Phase der Ausführung: Audrücke auswerten #
# =============================================== #
def evaluate(expr, env=global_env):
    match expr:
        # Einfache Werte
        case int(number) | float(number):
            return number
        # Variablen
        case str(name):
            # Variablen im Environment von vorne nach hinten
            # suchen
            for local_env in env:
                if name in local_env:
                    return local_env[name]

            # Nichts gefunden unter dem angegebenen Name: Error
            raise NameError(f"name '{name}' is not defined")

        #####################
        # Spezialkonstrukte #
        #####################
        # Wert abspeichern
        case ["sto", name, value]:
            value = evaluate(value, env)

            # Neue Variable im vordersten dict vom Environment
            # abspeichern
            local_env = env[0]
            local_env[name] = value
            return f"{name} stored: {value}"
        # Funktion definieren
        case ["phonk", [*params], body]:
            return ["phonk", params, body, env]
        # If
        case ["if", condition, true_body, false_body]:
            if evaluate(condition, env):
                return evaluate(true_body, env)
            else:
                return evaluate(false_body, env)

        #######################
        # Funktionen aufrufen #
        #######################
        case [operator, *args]:
            function = evaluate(operator, env)
            args = [evaluate(arg, env) for arg in args]
            match function:
                # "Eigene" Funktionen in unserer Sprache
                case ["phonk", params, body, closure_env]:
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
                    new_env = [local_env, *closure_env]

                    # Body in neuem Environment ausführen / evaluieren
                    return evaluate(body, new_env)

                # Eingebaute Funktionen (in Python geschrieben)
                case _:
                    return function(*args)

        # Unbekannter Ausdruck -> Fehler
        case _:
            raise ValueError("Unbekannter Ausdruck")

# =================================== #
# Hilfscode für die Konsole und Tests #
# =================================== #

def run(program):
    return evaluate(parse(tokenize(program)))

def repl():
    """Read-Eval-Print-Loop

    User-Eingabe analysieren und evaluieren.
    """
    run(library)

    while True:
        try:
            prog = input('> ').strip()
            if prog.lower() in ('q', 'quit', 'exit'):
                break
            print(run(prog))
        except Exception as e:
            print(f'{type(e).__name__}: {e}')


if __name__ == '__main__':
    # Testcode
    tests = [
        (tokenize, ('(+ 1 1)',), ['(', '+', '1', '1', ')']),
        (parse_atom, ('1.1',), 1.1),
        (parse, (['(', '+', '1', '1', ')'],), ['+', 1, 1]),
        (add, (1, 1), 2),
        (sub, (2, 1), 1),
        (mult, (2, 3), 6),
        (div, (7, 2), 3.5),
        (evaluate, (42,), 42),
        (evaluate, (['+', 40, 2],), 42),
        (evaluate, (['+', 40, ['+', 1, 1]],), 42),
        (evaluate, (['*', ['+', 5, 9], ['-', 11, ['/', 128, 16]]],), 42),
    ]
    ok = True
    for func, args, expected_out in tests:
        try:
            actual_out = func(*args)
            if actual_out == expected_out:
                print(func.__name__, 'OK')
            else:
                ok = False
                print(func.__name__, 'not OK!', actual_out, '!=', expected_out)
        except Exception as e:
            ok = False
            print(func.__name__, 'not OK!, Failure:', e)

    if ok:
        print('Alles OK!')
        print()
        print("Drücke 'q' um zu beenden..")
        repl()
    else:
        print('Es scheint noch nicht alles ok zu sein. Korrigiere die oben angezeigten Fehler.')
