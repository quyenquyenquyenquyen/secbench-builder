from tree_sitter import Language, Parser
import tree_sitter_javascript as tsjavascript
import tree_sitter_typescript as tstypescript
import tree_sitter_python as tspython
import tree_sitter_java as tsjava
import tree_sitter_cpp as tscpp

try:
    # Try to load standard TypeScript grammar
    TS_LANG = Language(tstypescript.language_typescript())
    # Try to load TSX grammar (for React)
    TSX_LANG = Language(tstypescript.language_tsx())
except AttributeError:
    # Fallback for some older versions 
    TS_LANG = Language(tstypescript.language())
    TSX_LANG = TS_LANG

LANGUAGES = {
    'javascript': Language(tsjavascript.language()),
    'typescript': TS_LANG,
    'tsx': TSX_LANG, # Add a separate parser for TSX
    'python': Language(tspython.language()),
    'java': Language(tsjava.language()),
    'cpp': Language(tscpp.language()),
    'c': Language(tscpp.language())
}

# --- 2. Function to get Parser by language ---
def get_parser_for_lang(lang_name):
    if lang_name in LANGUAGES:
        return Parser(LANGUAGES[lang_name])
    return None

def remove_comments(file_content: str, extension: str) -> str:
    """
    Remove comments for all supported languages.
    """
    if not file_content:
        return ""

    # Normalize extension (e.g., .jsx -> javascript)
    ext = extension.lower().replace('.', '')
    
    # Mapping logic (Updated to support TSX separately)
    lang_map = {
        'js': 'javascript', 'jsx': 'javascript', 'mjs': 'javascript',
        'ts': 'typescript', 
        'tsx': 'tsx', # TSX uses a separate parser
        'py': 'python',
        'java': 'java',
        'cpp': 'cpp', 'cc': 'cpp', 'cxx': 'cpp',
        'c': 'c'
    }
    
    lang_name = lang_map.get(ext)
    parser = get_parser_for_lang(lang_name)
    
    # If parser is not supported, return original code to ensure no data loss
    if not parser:
        return file_content

    # Encode to bytes for Tree-sitter processing
    byte_src = bytes(file_content, "utf8")
    tree = parser.parse(byte_src)
    
    comments = []
    def traverse(node):
        # Tree-sitter uses a label containing 'comment' for most languages
        if 'comment' in node.type:
            comments.append(node)
        for child in node.children:
            traverse(child)
    
    traverse(tree.root_node)
    
    # Remove from bottom to top to prevent index shifting
    sorted_comments = sorted(comments, key=lambda x: x.start_byte, reverse=True)
    byte_list = list(byte_src)
    
    for comment in sorted_comments:
        for i in range(comment.start_byte, comment.end_byte):
            if byte_list[i] != 10: # Keep newline \n (ASCII 10)
                byte_list[i] = 32 # Replace comment content with spaces (ASCII 32)
                
    return bytes(byte_list).decode("utf8")