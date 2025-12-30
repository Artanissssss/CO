class TypeChecker:
    def __init__(self, parse_tree, level=1):
        self.parse_tree = parse_tree
        self.level = level
        self.symbol_table = {}  # For variables and functions (Level 3+)
    
    def check(self):
        """Perform type checking on the parse tree"""
        self._annotate_types(self.parse_tree)
        return self.parse_tree
    
    def _annotate_types(self, node):
        """Recursively annotate types on parse tree nodes"""
        if node is None:
            return None
        
        # First, annotate all children
        for child in node.children:
            self._annotate_types(child)
        
        # Then determine type for this node based on grammar rule
        node_type = self._determine_type(node)
        node.type = node_type
        
        return node_type
    
    def _determine_type(self, node):
        """Determine type based on node name and children types"""
        name = node.name
        
        # Terminals
        if name == 'num_lit':
            return 'num'
        elif name == 'bool_lit':
            return 'bool'
        elif name in ['+', '*', '(', ')', '.', 'Compute', ',', '<', '=', 
                      'Let', 'be', 'if', 'then', 'else', 'maps', 'to', '>>']:
            return 'NA'
        
        # Non-terminals
        elif name == 'Z':
            # Z -> L
            if node.children and len(node.children) > 0:
                return node.children[0].type
            return 'NA'
        
        elif name == 'L':
            # L -> C or L -> S C
            for child in node.children:
                if child.name == 'C':
                    return child.type
            return 'NA'
        
        elif name == 'C':
            # C -> Compute E .
            for child in node.children:
                if child.name == 'E':
                    if child.type == 'TYPE_ERROR':
                        return 'TYPE_ERROR'
            return 'NA'
        
        elif name == 'E':
            # E -> A or E -> if B then A else A
            if len(node.children) == 1:
                # E -> A
                return node.children[0].type
            else:
                # E -> if B then A else A
                # Find B and both A nodes
                a_types = []
                b_type = None
                for child in node.children:
                    if child.name == 'A':
                        a_types.append(child.type)
                    elif child.name == 'B':
                        b_type = child.type
                
                if b_type != 'bool' and b_type != 'TYPE_ERROR':
                    return 'TYPE_ERROR'
                
                if len(a_types) == 2:
                    if a_types[0] == a_types[1] and a_types[0] != 'TYPE_ERROR':
                        return a_types[0]
                
                return 'TYPE_ERROR'
        
        elif name == 'B':
            # B -> P < P or B -> P = P or B -> P
            if len(node.children) == 1:
                # B -> P
                return node.children[0].type
            else:
                # B -> P < P or B -> P = P
                return 'bool'
        
        elif name == 'A':
            # A -> A + M or A -> M
            if len(node.children) == 1:
                # A -> M
                return node.children[0].type
            else:
                # A -> A + M
                a_type = node.children[0].type
                m_type = node.children[2].type if len(node.children) > 2 else None
                
                if a_type == 'num' and m_type == 'num':
                    return 'num'
                else:
                    return 'TYPE_ERROR'
        
        elif name == 'M':
            # M -> M * U or M -> U
            if len(node.children) == 1:
                # M -> U
                return node.children[0].type
            else:
                # M -> M * U
                m_type = node.children[0].type
                u_type = node.children[2].type if len(node.children) > 2 else None
                
                if m_type == 'num' and u_type == 'num':
                    return 'num'
                else:
                    return 'TYPE_ERROR'
        
        elif name == 'U':
            # U -> P or U -> U P (Level 4)
            if len(node.children) == 1:
                return node.children[0].type
            else:
                # Function application (Level 4)
                return 'num'  # Simplified for now
        
        elif name == 'P':
            # P -> num_lit, bool_lit, id, ( E )
            if len(node.children) == 1:
                return node.children[0].type
            elif len(node.children) == 3:
                # P -> ( E )
                return node.children[1].type
            return 'NA'
        
        elif name == 'S':
            # S -> S D or S -> D (Level 3)
            return 'NA'
        
        elif name == 'D':
            # D -> Let T id be E . (Level 3)
            return 'NA'
        
        elif name == 'T':
            # T -> num or T -> bool
            return 'NA'
        
        elif name == 'id':
            # Variable reference (Level 3+)
            if self.level >= 3:
                var_type = self.symbol_table.get(node.lexeme)
                if var_type:
                    return var_type
            return 'num'  # Default for now
        
        else:
            return 'NA'
    
    def node_to_dict(self, node):
        """Convert typed parse tree node to dictionary"""
        if node is None:
            return None
        
        result = {"name": node.name, "type": getattr(node, 'type', 'NA')}
        
        if node.lexeme is not None:
            result["lexeme"] = node.lexeme
        
        if node.children:
            result["children"] = [self.node_to_dict(child) for child in node.children]
        
        return result
