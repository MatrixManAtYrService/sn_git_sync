import sn_git
import unittest

import ipdb
import IPython
def undebug():
    def f() : pass
    ipdb.set_trace = f
    IPython.embed = f

class ArgsTest(unittest.TestCase):

    # correct callback gets called with correct repo name
    def test_repo_name_argparse(self):
        parser = sn_git.cmd.Parser(
                "cmdName",
                "some/dir",
                lambda args : self.assertEqual(args.repo_name, "foo"),
                lambda : None)
        parser.parse(['configure', 'foo', 'bar'])

    # correct callback gets called with correct repo url
    def test_repo_url_argparse(self):
        parser = sn_git.cmd.Parser(
                "cmdName",
                "some/dir",
                lambda args : self.assertEqual(args.repo_url, "bar"),
                lambda : None)
        parser.parse(['configure', 'foo', 'bar'])

    # correct callback gets called with correct repo url
    def test_sn_user_argparse(self):
        parser = sn_git.cmd.Parser(
                "cmdName",
                "some/dir",
                lambda : None,
                lambda args : self.assertEqual(args.sn_user, "foo"))
        parser.parse(['sync', 'foo', 'bar'])

    # correct callback gets called with correct password
    def test_sn_pass_argparse(self):
        parser = sn_git.cmd.Parser(
                "cmdName",
                "some/dir",
                lambda : None,
                lambda args : self.assertEqual(args.sn_pass, "bar"))
        parser.parse(['sync', 'foo', 'bar'])


