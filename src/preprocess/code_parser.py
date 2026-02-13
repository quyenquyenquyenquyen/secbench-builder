from tree_sitter import Language, Parser
import tree_sitter_javascript as tsjavascript

# --- 1. Language Configuration (Initialize once) ---
try:
    # For newer tree-sitter versions
    JS_LANGUAGE = Language(tsjavascript.language())
except Exception:
    # Fallback for older versions
    JS_LANGUAGE = Language(tsjavascript.language(), "javascript")

# Initialize global Parser to optimize performance (avoid re-init multiple times)
parser = Parser(JS_LANGUAGE)

# --- 2. Comment Removal Function (Extracted for direct import) ---
def remove_comments(file_content: str) -> str:
    """
    Use Tree-sitter to parse and remove comments, keeping the code intact.
    """
    if not file_content:
        return ""

    # Tree-sitter works with bytes
    byte_src = bytes(file_content, "utf8")
    
    # Parse code
    tree = parser.parse(byte_src)
    root_node = tree.root_node
    
    comments = []
    
    # Recursive function to traverse AST and find comment nodes
    def traverse(node):
        # Node types defined as comments in JS Grammar
        if node.type in ['comment', 'line_comment', 'block_comment', 'hash_comment']:
            comments.append(node)
        for child in node.children:
            traverse(child)
    
    traverse(root_node)
    
    # Sort comments from bottom to top so removal doesn't shift indices of upper comments
    sorted_comments = sorted(comments, key=lambda x: x.start_byte, reverse=True)
    
    # Convert bytes to list for mutability
    byte_list = list(byte_src)
    
    for comment in sorted_comments:
        # Replace comment content with whitespace (Space)
        # This helps preserve line numbers for easier debugging
        for i in range(comment.start_byte, comment.end_byte):
            # 32 is ASCII for space, 10 is newline (\n)
            # If comment has newlines, keep them to preserve file structure
            if byte_list[i] != 10: 
                byte_list[i] = 32 
    
    # Convert back to string
    return bytes(byte_list).decode("utf8")