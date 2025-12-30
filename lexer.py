import re

class Token:
    def __init__(self, name, lexeme):
        self.name = name
        self.lexeme = lexeme
    
    def to_dict(self):
        return {"name": self.name, "lexeme": self.lexeme}

class Lexer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.position = 0
        self.tokens_list = []
        
        # Define keywords
        self.keywords = {
            'Compute', 'Let', 'be', 'if', 'then', 'else', 
            'maps', 'to', 'num', 'bool', 'true', 'false'
        }
    
    def tokenize(self):
        """Tokenize the source code and return list of tokens"""
        while self.position < len(self.source_code):
            # Skip whitespace
            if self.source_code[self.position].isspace():
                self.position += 1
                continue
            
            # Try to match tokens
            if self._match_keyword_or_identifier():
                continue
            elif self._match_number():
                continue
            elif self._match_operator():
                continue
            elif self._match_delimiter():
                continue
            else:
                # Unknown character, skip it
                self.position += 1
        
        return self.tokens_list
    
    def _match_keyword_or_identifier(self):
        """Match keywords, boolean literals, or identifiers"""
        if not self.source_code[self.position].isalpha():
            return False
        
        start = self.position
        while self.position < len(self.source_code) and \
              (self.source_code[self.position].isalnum() or self.source_code[self.position] == '_'):
            self.position += 1
        
        lexeme = self.source_code[start:self.position]
        
        # Check if it's a boolean literal
        if lexeme == 'true' or lexeme == 'false':
            self.tokens_list.append(Token('bool_lit', lexeme))
        elif lexeme in self.keywords:
            self.tokens_list.append(Token(lexeme, lexeme))
        else:
            # It's an identifier
            self.tokens_list.append(Token('id', lexeme))
        
        return True
    
    def _match_number(self):
        """Match number literals"""
        if not self.source_code[self.position].isdigit():
            return False
        
        start = self.position
        while self.position < len(self.source_code) and \
              self.source_code[self.position].isdigit():
            self.position += 1
        
        lexeme = self.source_code[start:self.position]
        self.tokens_list.append(Token('num_lit', lexeme))
        return True
    
    def _match_operator(self):
        """Match operators: +, *, <, =, >>"""
        # Check for >> (two characters)
        if self.position + 1 < len(self.source_code) and \
           self.source_code[self.position:self.position+2] == '>>':
            self.tokens_list.append(Token('>>', '>>'))
            self.position += 2
            return True
        
        # Single character operators
        if self.source_code[self.position] in ['+', '*', '<', '=']:
            op = self.source_code[self.position]
            self.tokens_list.append(Token(op, op))
            self.position += 1
            return True
        
        return False
    
    def _match_delimiter(self):
        """Match delimiters: (, ), ,, ."""
        if self.source_code[self.position] in ['(', ')', ',', '.']:
            delim = self.source_code[self.position]
            self.tokens_list.append(Token(delim, delim))
            self.position += 1
            return True
        
        return False
    
    def tokens(self):
        """Return the list of tokens"""
        return self.tokenize()
