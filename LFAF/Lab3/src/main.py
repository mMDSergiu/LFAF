#this class represents a token with its type and value
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    #this method defines how a token will be printed
    def __str__(self):
        return f"{self.type} -> {self.value}"


#this class performs lexical analysis and converts text into tokens
class Lexer:

    #initializes the lexer with the input text and prepares the first character
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current_char = self.text[self.position] if text else None

    #moves the pointer to the next character in the input
    def advance(self):
        self.position += 1
        if self.position < len(self.text):
            self.current_char = self.text[self.position]
        else:
            self.current_char = None

    #skips any whitespace characters in the input
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    #reads a number from the input and determines if it is an integer or float
    def number(self):
        result = ""
        dot_count = 0

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == "."):
            if self.current_char == ".":
                dot_count += 1
            result += self.current_char
            self.advance()

        if dot_count == 1:
            return Token("FLOAT", result)
        else:
            return Token("INTEGER", result)

    #reads identifiers such as function names like sin or cos
    def identifier(self):
        result = ""

        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()

        if result == "sin":
            return Token("SIN", result)
        elif result == "cos":
            return Token("COS", result)
        else:
            return Token("IDENTIFIER", result)

    #main function that scans the input and returns tokens one by one
    def get_next_token(self):

        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha():
                return self.identifier()

            if self.current_char == "+":
                self.advance()
                return Token("PLUS", "+")

            if self.current_char == "-":
                self.advance()
                return Token("MINUS", "-")

            if self.current_char == "*":
                self.advance()
                return Token("MULTIPLY", "*")

            if self.current_char == "/":
                self.advance()
                return Token("DIVIDE", "/")

            if self.current_char == "(":
                self.advance()
                return Token("LPAREN", "(")

            if self.current_char == ")":
                self.advance()
                return Token("RPAREN", ")")

            raise Exception(f"Invalid character: {self.current_char}")

        return Token("EOF", None)


#runs the lexer and prints all tokens from the input
def run_lexer(text):
    lexer = Lexer(text)

    while True:
        token = lexer.get_next_token()
        if token.type == "EOF":
            break
        print(token)


#program entry point that asks the user for an expression
if __name__ == "__main__":
    expression = input("Enter expression: ")

    print("\nTokens:")
    run_lexer(expression)
