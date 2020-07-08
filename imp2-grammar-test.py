import unittest
import tatsu                            # Tatsu is the parser generator.

class TestImpGrammar(unittest.TestCase):
    def setUp(self):
        imp_grammar_h = open('imp2.ebnf')
        imp_grammar = imp_grammar_h.read()
        imp_grammar_h.close()
        self.parser = tatsu.compile(imp_grammar)

    def __test_parse(self, file_name, ast):
        source_h = open(file_name)
        source = source_h.read()
        source_h.close()
        self.assertEqual(str(self.parser.parse(source)), ast)

    def test_exp_parse0(self):
        self.__test_parse('examples/exp-test0.imp2', "AST({'ds': [], 'cs': AST({'ac': AST({'idn': 'x', 'op': ':=', 'e': AST({'e': AST({'e1': '1', 'op': '<', 'e2': AST({'e': AST({'e': AST({'e1': '4', 'op': '*', 'e2': AST({'e': AST({'e1': '3', 'op': '/', 'e2': '3'})})})})})})})})})})")

    def test_exp_parse1(self):
        self.__test_parse('examples/exp-test1.imp2',"AST({'ds': AST({'d': AST({'op': 'var', 'idn': 'y', 'e': AST({'e1': 'True', 'op': 'and', 'e2': AST({'e': AST({'e1': 'z', 'op': 'and', 'e2': AST({'e': AST({'op': 'not', 'e': 'True'})})})})})})})})")

    def test_exp_parse2(self):
        self.__test_parse('examples/exp-test2.imp2', "AST({'ds': [], 'cs': AST({'ac': AST({'idn': 'x', 'op': ':=', 'e': AST({'e1': '4', 'op': '-', 'e2': AST({'e': AST({'e1': '2', 'op': '+', 'e2': '2'})})})})})})")

    def test_exp_parse3(self):
        self.__test_parse('examples/exp-test3.imp2', "AST({'ds': [], 'cs': AST({'ac': AST({'idn': 'x', 'op': ':=', 'e': AST({'e1': '2', 'op': '>', 'e2': AST({'e': AST({'e1': 'x', 'op': '+', 'e2': '1'})})})})})})")

    def test_exp_parse4(self):
        self.__test_parse('examples/exp-test4.imp2',"AST({'ds': [], 'cs': AST({'ac': AST({'idn': 'x', 'op': ':=', 'e': AST({'e1': '4', 'op': '+', 'e2': AST({'e1': '3', 'op': '-', 'e2': '5'})})})})})")

    def test_cmd_parse0(self):
        self.__test_parse('examples/cmd-test0.imp2', "AST({'ds': AST({'d': AST({'op': 'var', 'idn': ['x', 'y'], 'e': ['10', '1']})}), 'cs': AST({'ac': AST({'op': 'while', 't': AST({'e': AST({'e1': 'x', 'op': '>', 'e2': '0'})}), 'b': AST({'ds': [], 'cs': AST({'ac': [AST({'idn': 'y', 'op': ':=', 'e': AST({'e1': 'y', 'op': '*', 'e2': 'x'})}), AST({'idn': 'x', 'op': ':=', 'e': AST({'e1': 'x', 'op': '-', 'e2': '1'})})]})})})})})")

    def test_cmd_parse1(self):
        self.__test_parse('examples/cmd-test1.imp2',"AST({'ds': AST({'d': AST({'op': 'var', 'idn': ['x', 'y', 'z'], 'e': ['1', '0', '0']})}), 'cs': AST({'ac': [AST({'idn': 'x', 'op': ':=', 'e': '0'}), AST({'idn': 'y', 'op': ':=', 'e': '1'}), AST({'idn': 'z', 'op': ':=', 'e': '3'}), AST({'op': 'if', 't': AST({'e': AST({'e1': 'x', 'op': '<', 'e2': '2'})}), 'b1': AST({'ds': [], 'cs': AST({'ac': AST({'idn': 'z', 'op': ':=', 'e': '3'})})})})]})})")

    def test_def_parse0(self):
        self.__test_parse('examples/def-test0.imp2', "AST({'ds': AST({'d': AST({'op': 'def', 'idn': 'fat', 'f': ['x'], 'b': AST({'ds': AST({'d': [AST({'op': 'var', 'idn': 'z', 'e': 'x'}), AST({'op': 'var', 'idn': 'y', 'e': '1'})]}), 'cs': AST({'ac': AST({'op': 'while', 't': AST({'e': AST({'e1': 'z', 'op': '>', 'e2': '0'})}), 'b': AST({'ds': [], 'cs': AST({'ac': [AST({'idn': 'y', 'op': ':=', 'e': AST({'e1': 'y', 'op': '*', 'e2': 'z'})}), AST({'idn': 'z', 'op': ':=', 'e': AST({'e1': 'z', 'op': '-', 'e2': '1'})})]})})})})})})}), 'cs': AST({'ac': AST({'idn': 'fat', 'a': ['10']})})})")

    def test_def_parse1(self):
        self.__test_parse('examples/def-test1.imp2',"AST({'ds': AST({'d': AST({'op': 'def', 'idn': 'fat', 'f': ['x', ',', 'y'], 'b': AST({'ds': [], 'cs': AST({'ac': AST({'op': 'if', 't': AST({'e': AST({'e1': 'x', 'op': '>', 'e2': '0'})}), 'b1': AST({'ds': [], 'cs': AST({'ac': AST({'idn': 'fat', 'a': [AST({'e1': 'x', 'op': '-', 'e2': '1'}), ',', AST({'e1': 'y', 'op': '*', 'e2': 'x'})]})})})})})})})}), 'cs': AST({'ac': AST({'idn': 'fat', 'a': ['10', ',', '1']})})})")
        
if __name__ == '__main__':
    unittest.main()
