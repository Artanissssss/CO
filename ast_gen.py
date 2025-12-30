class ASTNode:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children if children is not None else []
    
    def to_dict(self):
        """Convert AST node to dictionary for JSON output"""
        result = {"name": self.name}
        if self.children:
            result["children"] = [child.to_dict() for child in self.children]
        return result

class ASTGenerator:
    def __init__(self, parse_tree):
        self.parse_tree = parse_tree
    
    def generate(self):
        """Generate AST from parse tree"""
        return self._simplify(self.parse_tree)
    
    def _simplify(self, node):
        """Recursively simplify parse tree to AST"""
        if node is None:
            return None
        
        name = node.name
        
        # Handle terminals - convert to leaf nodes
        if name in ['num_lit', 'bool_lit', 'id']:
            return ASTNode(node.lexeme)
        
        # Handle operators - create operator nodes
        if name == 'C':
            # C -> Compute E .
            # Create Compute node with E as child
            for child in node.children:
                if child.name == 'E':
                    e_ast = self._simplify(child)
                    return ASTNode('Compute', [e_ast] if e_ast else [])
            return ASTNode('Compute')
        
        elif name == 'A':
            # A -> A + M or A -> M
            if len(node.children) == 3:
                # A -> A + M
                left = self._simplify(node.children[0])
                right = self._simplify(node.children[2])
                return ASTNode('+', [left, right])
            else:
                # A -> M
                return self._simplify(node.children[0])
        
        elif name == 'M':
            # M -> M * U or M -> U
            if len(node.children) == 3:
                # M -> M * U
                left = self._simplify(node.children[0])
                right = self._simplify(node.children[2])
                return ASTNode('*', [left, right])
            else:
                # M -> U
                return self._simplify(node.children[0])
        
        elif name == 'E':
            # E -> A or E -> if B then A else A
            if len(node.children) == 1:
                # E -> A
                return self._simplify(node.children[0])
            else:
                # E -> if B then A else A
                # Create if node with condition and branches
                cond = None
                then_branch = None
                else_branch = None
                
                i = 0
                while i < len(node.children):
                    child = node.children[i]
                    if child.name == 'if':
                        i += 1
                        if i < len(node.children):
                            cond = self._simplify(node.children[i])
                    elif child.name == 'then':
                        i += 1
                        if i < len(node.children):
                            then_branch = self._simplify(node.children[i])
                    elif child.name == 'else':
                        i += 1
                        if i < len(node.children):
                            else_branch = self._simplify(node.children[i])
                    elif child.name == 'B':
                        cond = self._simplify(child)
                    elif child.name == 'A':
                        if then_branch is None:
                            then_branch = self._simplify(child)
                        else:
                            else_branch = self._simplify(child)
                    i += 1
                
                children = []
                if cond:
                    children.append(cond)
                if then_branch:
                    children.append(then_branch)
                if else_branch:
                    children.append(else_branch)
                
                return ASTNode('if', children)
        
        elif name == 'B':
            # B -> P < P or B -> P = P or B -> P
            if len(node.children) == 3:
                op = node.children[1].name
                left = self._simplify(node.children[0])
                right = self._simplify(node.children[2])
                return ASTNode(op, [left, right])
            else:
                return self._simplify(node.children[0])
        
        elif name == 'P':
            # P -> ( E ) or P -> num_lit or P -> bool_lit or P -> id
            if len(node.children) == 3:
                # P -> ( E )
                return self._simplify(node.children[1])
            else:
                return self._simplify(node.children[0])
        
        elif name in ['U', 'L', 'Z', 'S', 'D', 'T', 'F', 'G', 'I']:
            # Pass through - simplify children
            for child in node.children:
                result = self._simplify(child)
                if result:
                    return result
            return None
        
        # Default: return first non-terminal child
        for child in node.children:
            if child.name not in ['+', '*', '(', ')', '.', ',', '<', '=', 
                                   'Compute', 'if', 'then', 'else', 'Let', 'be',
                                   'maps', 'to', 'num', 'bool', '>>']:
                result = self._simplify(child)
                if result:
                    return result
        
        return None
