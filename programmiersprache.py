def tokenize(program):
    """Programmtext in die logischen Blöcke aufteilen.
    """
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

def fact(a):
    if a < 2:
        return 1
    else:
        return a * fact(a - 1)

def block(*args):
    if len(args) == 0:
        return None
    else:
        return args[-1]

import math
import random

# Eingebaute Funktionen
builtins = {
    "+": add,
    "-": sub,
    "*": mult,
    "/": div,
    "//": div_int,
    "expt": expt,
    "fact": fact,
    "sin": math.sin,
    "e": math.e,
    "random": random.random,
    "block": block,
}

# Library (in unserer Sprache geschriebener Code)
library = """
(block
    (sto pi 3.141592653589793)
    (sto cos (phonk (a) (sin (+ a (/ pi 2)))))

)
"""

# Globales Environment
global_env = [{}, builtins]

def evaluate(expr, env=global_env):
    match expr:
        # Einfache Werte
        case int(number) | float(number):
            return number
        case str(name):
            # Variablen im Environment von vorne nach hinten
            # suchen
            for local_env in env:
                if name in local_env:
                    return local_env[name]

            # Nichts gefunden unter dem angegebenen Name: Error
            raise NameError(f"name '{name}' is not defined")

        # Spezialkonstrukte
        case ["sto", name, value]:     # Wert abspeichern
            value = evaluate(value, env)

            # Neue Variable im vordersten dict vom Environment
            # abspeichern
            local_env = env[0]
            local_env[name] = value
            return f"{name} stored: {value}"
        case ["phonk", [*params], body]:  # Funktionsdefinition
            return ["phonk", params, body]

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

        # Unbekannter Ausdruck -> Fehler
        case _:
            raise ValueError("Unbekannter Ausdruck")

#=====================
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
