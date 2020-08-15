import unittest
import tatsu
from impiler import Impiler
from pi import run


class TestImpToPiIRAbs(unittest.TestCase):
    def setUp(self):
        imp_grammar_h = open('imp2.ebnf')
        imp_grammar = imp_grammar_h.read()
        imp_grammar_h.close()
        self.parser = tatsu.compile(imp_grammar)

    def __test_parse(self, file_name, ast):
        source_h = open(file_name)
        source = source_h.read()
        source_h.close()
        pi_ast = self.parser.parse(source, semantics=Impiler())
        self.assertEqual(str(pi_ast), ast)

    def __test_run(self, file_name, s, locs, env, sto, val, cnt):
        source_h = open(file_name)
        source = source_h.read()
        source_h.close()
        pi_ast = self.parser.parse(source, semantics=Impiler())
        (tr, ns, dt) = run(pi_ast, color=False)
        state_str = tr[s]
        loc_str = "locs : " + locs
        env_str = "env : " + env
        sto_str = "sto : " + sto
        val_str = "val : " + val
        cnt_str = "cnt : " + cnt
        self.assertTrue(loc_str in state_str)
        self.assertTrue(env_str in state_str)
        self.assertTrue(sto_str in state_str)
        self.assertTrue(val_str in state_str)
        self.assertTrue(cnt_str in state_str)

    def test_fat(self):
        self.__test_parse(
            'examples/fat.imp2', "Blk(DSeq(Bind(Id(z), Ref(1)), BindAbs(Id(fat), Abs([Id(x)], Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop()))))), Call(Id(fat), [10]))")

    def test_regra_35(self):
        # Em qual estado a regra 35 (slide 30) é aplicada no exemplo do fatorial?
        s = 8
        # Qual o estado do componente locs (BlockLocs) em s?
        locs = "[0]"
        # Qual o estado do componente env (Ambiente) em s?
        env = "{}"
        # Qual o estado do componente sto (Memória) em s?
        sto = "{0: 1}"
        # Qual o estado do componente val (Pilha de valores) em s?
        val = "[[], Call(Id(fat), [10]), {'z': 0}, Id(fat), {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}]"
        # Qual o estado do componente cnt (Pilha de controle) em s?
        cnt = "['#BLKDEC', '#DSEQ', '#BIND']"
        self.__test_run('examples/fat.imp2', s, locs, env, sto, val, cnt)

    def test_regra_menor_36(self):
        # Qual o menor estado no qual a regra 36 (slide 30) é aplicada no exemplo do fatorial?
        s = 12
        # Qual o estado do componente locs (BlockLocs) em s?
        locs = "[0]"
        # Qual o estado do componente env (Ambiente) em s?
        env = "{'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}}"
        # Qual o estado do componente sto (Memória) em s?
        sto = "{0: 1}"
        # Qual o estado do componente val (Pilha de valores) em s?
        val = "[[], {}, Id(fat)]"
        # Qual o estado do componente cnt (Pilha de controle) em s?
        cnt = "['#BLKCMD', '#CALL', 10]"
        self.__test_run('examples/fat.imp2', s, locs, env, sto, val, cnt)

    def test_regra_maior_36(self):
        # Qual o maior estado no qual a regra 36 (slide 30) é aplicada no exemplo do fatorial?
        s = 219
        # Qual o estado do componente locs (BlockLocs) em s?
        locs = "[]"
        # Qual o estado do componente env (Ambiente) em s?
        env = "{'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 1}"
        # Qual o estado do componente sto (Memória) em s?
        sto = "{0: 3628800}"
        # Qual o estado do componente val (Pilha de valores) em s?
        val = "[[], {}, [0], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}}, [0], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 10}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 10}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 10}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 9}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 9}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 9}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 8}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 8}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 8}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 7}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 7}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 7}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 6}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 6}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 6}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 5}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 5}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 5}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 4}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 4}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 4}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 3}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 3}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 3}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 2}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 2}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 2}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 1}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 1}, Id(fat)]"
        # Qual o estado do componente cnt (Pilha de controle) em s?
        cnt = "['#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#CALL', Sub(Id(x), 1)]"
        self.__test_run('examples/fat.imp2', s, locs, env, sto, val, cnt)

    def test_regra_menor_37(self):
        # Qual o menor estado no qual a regra 36 (slide 30) é aplicada no exemplo do fatorial?
        s = 14
        # Qual o estado do componente locs (BlockLocs) em s?
        locs = "[0]"
        # Qual o estado do componente env (Ambiente) em s?
        env = "{'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 10}"
        # Qual o estado do componente sto (Memória) em s?
        sto = "{0: 1}"
        # Qual o estado do componente val (Pilha de valores) em s?
        val = "[[], {}, [0], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}}]"
        # Qual o estado do componente cnt (Pilha de controle) em s?
        cnt = "['#BLKCMD', '#BLKCMD', Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop()))]"
        self.__test_run('examples/fat.imp2', s, locs, env, sto, val, cnt)

    def test_regra_maior_37(self):
        # Qual o maior estado no qual a regra 36 (slide 30) é aplicada no exemplo do fatorial?
        s = 224
        # Qual o estado do componente locs (BlockLocs) em s?
        locs = "[]"
        # Qual o estado do componente env (Ambiente) em s?
        env = "{'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 0}"
        # Qual o estado do componente sto (Memória) em s?
        sto = "{0: 3628800}"
        # Qual o estado do componente val (Pilha de valores) em s?
        val = "[[], {}, [0], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}}, [0], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 10}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 10}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 10}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 9}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 9}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 9}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 8}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 8}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 8}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 7}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 7}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 7}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 6}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 6}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 6}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 5}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 5}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 5}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 4}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 4}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 4}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 3}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 3}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 3}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 2}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 2}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 2}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 1}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 1}, [], {'z': 0, 'fat': {'for': [Id(x)], 'block': Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop())), 'env': {}}, 'x': 1}]"
        # Qual o estado do componente cnt (Pilha de controle) em s?
        cnt = "['#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', '#BLKCMD', Blk(Cond(Gt(Id(x), 0), Blk(CSeq(Assign(Id(z), Mul(Id(z), Id(x))), Call(Id(fat), [Sub(Id(x), 1)]))), Nop()))]"
        self.__test_run('examples/fat.imp2', s, locs, env, sto, val, cnt)


if __name__ == '__main__':
    unittest.main()
