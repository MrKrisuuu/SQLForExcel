from scanner import lexer


if __name__ == '__main__':
    filename = "tests/selects.sql"
    file = open(filename, "r")

    text = file.read()
    lexer = lexer
    lexer.input(text)  # Give the lexer some input

    while True:
        tok = lexer.token()
        if not tok:
            break    # No more input
        print(f"{tok.lineno} {tok.type}({tok.value})")

    file.close()
