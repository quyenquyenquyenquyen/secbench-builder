import unittest
from src.preprocess.code_parser import remove_comments

class TestCodeParser(unittest.TestCase):
    
    def test_javascript_comments(self):
        code = "var x = 1; // line comment\n/* block \n comment */ var y = 2;"
        
        # "// line comment" has exactly 15 characters (2 slashes + 1 space + 4 letters 'line' + 1 space + 7 letters 'comment')
        line1_spaces = " " * 15  
        
        block_part1_spaces = " " * 9   # "/* block " (9 characters)
        block_part2_spaces = " " * 11  # " comment */" (11 characters)
        
        expected = f"var x = 1; {line1_spaces}\n{block_part1_spaces}\n{block_part2_spaces} var y = 2;"
        
        self.assertEqual(remove_comments(code, 'js'), expected)

    def test_python_comments(self):
        code = "def hello():\n    # This is a comment\n    print('hi')"
        # "# This is a comment" is 19 characters long
        comment_spaces = " " * 19
        expected = f"def hello():\n    {comment_spaces}\n    print('hi')"
        self.assertEqual(remove_comments(code, 'py'), expected)

    def test_java_comments(self):
        code = "public class Main {\n    // Java comment\n    int x = 0;\n}"
        # "// Java comment" is 15 characters long
        comment_spaces = " " * 15
        expected = f"public class Main {{\n    {comment_spaces}\n    int x = 0;\n}}"
        self.assertEqual(remove_comments(code, 'java'), expected)

    def test_unsupported_lang(self):
        code = "some random code # comment"
        self.assertEqual(remove_comments(code, 'xyz'), code)

if __name__ == '__main__':
    unittest.main()