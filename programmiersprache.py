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

operators = {
    "+": add,
}

def evaluate(expr):
    if isinstance(expr, int) or isinstance(expr, float):
        return expr
    elif isinstance(expr, list):
        operator = expr[0]
        function = operators[operator]
        args = expr[1:]
        args = [evaluate(arg) for arg in args]
        return function(*args)

print(evaluate(parse(tokenize("1"))))                     # -> 1
print(evaluate(parse(tokenize("(+ 1 1)"))))               # -> 2
print(evaluate(parse(tokenize("(+ (+ 1 2) (+ 3 4))"))))   # -> 10



#=====================
def repl():
    """Read-Eval-Print-Loop
    
    Usereingabe analysieren und evaluieren.
    """
    while True:
        try:
            prog = input('> ').strip()
            if prog.lower() in ('q', 'quit', 'exit'):
                break
            print(evaluate(parse(tokenize(prog))))
        except Exception as e:
            print(f'{type(e).__name__}: {e}')


if __name__ == '__main__':
    # Testcode
    tests = [
        (tokenize, ('(+ 1 1)',), ['(', '+', '1', '1', ')']),
        (parse, (['(', '+', '1', '1', ')'],), ['+', 1, 1]),
        (parse_atom, ('1.1',), 1.1),
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
