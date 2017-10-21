import sn_git
import unittest

import ipdb
import IPython
def undebug():
    def f() : pass
    ipdb.set_trace = f
    IPython.embed = f

class GitTest(unittest.TestCase):

    def setUp(self):
        self.gitAgent = sn_git.GitAgent(sn_git.config_dir, "test", "git@github.com:MatrixManAtYrService/notes_test.git")

    def test_push_pull(self):
        self.assertEqual(1,2)
