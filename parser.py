import csv

class ParseTreeNode:
    def __init__(self, name, lexeme=None, children=None):
        self.name = name
        self.lexeme = lexeme
        self.children = children if children is not None else []
    
    def to_dict(self):
        """Convert parse tree node to dictionary for JSON output"""
        result = {"name": self.name}
        if self.lexeme is not None:
            result["lexeme"] = self.lexeme
        if self.children:
            result["children"] = [child.to_dict() for child in self.children]
        return result

class Parser:
    def __init__(self, tokens, level=1):
        self.tokens = tokens
        self.level = level
        self.position = 0
        self.stack = [0]  # State stack for LR parsing
        self.symbol_stack = []  # Symbol stack
        self.action_table = {}
        self.goto_table = {}
        self.grammar = []
        
        # Load the parsing table and grammar for the specified level
        self._load_parsing_table(f'level{level}_parsing_table.csv')
        self._load_grammar(f'level{level}_grammar.txt')
    
    def _load_grammar(self, filename):
        """Load grammar rules from file"""
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line and '->' in line:
                    # Parse rule like "00.		Z -> L"
                    # Split by tabs to find the rule
                    parts = line.split('\t')
                    rule_text = None
                    
                    # Find the part with ->
                    for part in parts:
                        if '->' in part:
                            rule_text = part.strip()
                            break
                    
                    if rule_text and '->' in rule_text:
                        lhs, rhs = rule_text.split('->')
                        lhs = lhs.strip()
                        rhs = rhs.strip().split() if rhs.strip() else []
                        self.grammar.append((lhs, rhs))
    
    def _load_parsing_table(self, filename):
        """Load LR parsing table from CSV file"""
        with open(filename, 'r', encoding='utf-8') as f:
            # Detect delimiter by checking first line
            first_line = f.readline()
            f.seek(0)
            
            # Use comma if present, otherwise tab
            delimiter = ',' if ',' in first_line else '\t'
            
            reader = csv.reader(f, delimiter=delimiter)
            
            # Skip first header row ("State", "ACTION", "GOTO", etc.)
            next(reader)
            
            # Read second header row (actual symbols)
            headers = next(reader)
            
            for row in reader:
                if not row or not row[0].strip():
                    continue
                
                try:
                    state = int(row[0].strip())
                except ValueError:
                    continue
                
                # Process each column
                for i, cell in enumerate(row[1:], 1):
                    if i >= len(headers):
                        break
                    
                    symbol = headers[i].strip()
                    cell = cell.strip()
                    
                    if not cell or not symbol:
                        continue
                    
                    if cell.startswith('s'):
                        # Shift
                        self.action_table[(state, symbol)] = ('shift', int(cell[1:]))
                    elif cell.startswith('r'):
                        # Reduce
                        self.action_table[(state, symbol)] = ('reduce', int(cell[1:]))
                    elif cell == 'acc':
                        # Accept
                        self.action_table[(state, symbol)] = ('accept', None)
                    elif cell.isdigit():
                        # GOTO entry (for non-terminals)
                        self.goto_table[(state, symbol)] = int(cell)
    
    def parse(self):
        """Parse tokens using LR parsing algorithm"""
        # Add end-of-input marker
        tokens = self.tokens + [type('Token', (), {'name': '$', 'lexeme': '$'})()]
        
        i = 0  # Input pointer
        
        while True:
            state = self.stack[-1]
            current_token = tokens[i]
            
            # Look up action
            action = self.action_table.get((state, current_token.name))
            
            if action is None:
                raise SyntaxError(f"Parse error at token {current_token.name} in state {state}")
            
            action_type, action_value = action
            
            if action_type == 'shift':
                # Shift: push token and new state
                self.stack.append(action_value)
                node = ParseTreeNode(current_token.name, current_token.lexeme)
                self.symbol_stack.append(node)
                i += 1
            
            elif action_type == 'reduce':
                # Reduce by grammar rule
                lhs, rhs = self.grammar[action_value]
                
                # Pop symbols from stack
                children = []
                for _ in range(len(rhs)):
                    if self.stack:
                        self.stack.pop()
                    if self.symbol_stack:
                        children.insert(0, self.symbol_stack.pop())
                
                # Create new non-terminal node
                new_node = ParseTreeNode(lhs, children=children)
                self.symbol_stack.append(new_node)
                
                # Look up GOTO
                if self.stack:
                    goto_state = self.goto_table.get((self.stack[-1], lhs))
                    if goto_state is not None:
                        self.stack.append(goto_state)
            
            elif action_type == 'accept':
                # Accept: parsing complete
                # The symbol_stack should have the start symbol L
                # We need to reduce to Z (the augmented start symbol)
                if self.symbol_stack and self.symbol_stack[0].name == 'L':
                    # Do final reduction to Z
                    root = ParseTreeNode('Z', children=[self.symbol_stack[0]])
                    return root
                return self.symbol_stack[0] if self.symbol_stack else None
