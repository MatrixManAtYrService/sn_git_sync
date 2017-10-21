import sn_git
import shutil
import unittest
import os
from datetime import datetime
import calendar

import ipdb
import IPython
def undebug():
    def f() : pass
    ipdb.set_trace = f
    IPython.embed = f

class GitTest(unittest.TestCase):

    def _read_last_line(filename):
        with open(filename, "r") as f:
            lines = f.readlines()
            return lines[-1]

    def _write_last_line(filename, new_last_line):
        with open(filename, "r") as f:
            lines = f.readlines()
            lines[-1] = new_last_line
        with open(filename, "w") as f:
            f.writelines(lines)

    def test_round_trip(self):

        # some constant values we'll use
        this_dir = os.path.dirname(os.path.abspath(__file__))
        test_cfg = os.path.join(this_dir, 'testCfg')
        readme_path = os.path.join(test_cfg, 'test', 'README.md')
        d = datetime.utcnow()
        new_stamp = "last test: "\
                    + str(calendar.timegm(d.utctimetuple()))\
                    + "\n"

        # remove previous test directory
        try:
            shutil.rmtree(test_cfg)
        except FileNotFoundError:
                pass
        self.assertFalse(os.path.exists(test_cfg),
                msg="need blank slate for test, ./testCfg/ should now be gone")

        # initialize a git repo
        agent = sn_git.git.Agent(test_cfg, "test", "git@github.com:MatrixManAtYrService/sn_git_test.git")
        agent.configure_repo()
        self.assertTrue(os.path.exists(test_cfg),
                msg="After configuring repo, folder should exist: {}".format(test_cfg))
        self.assertTrue(os.path.exists(readme_path),
                msg="After fetchin repo, file from repo should exist: {}".format(readme_path))

        # update the time stamp
        old_stamp = GitTest._read_last_line(readme_path)
        GitTest._write_last_line(readme_path, new_stamp)

        new_stamp = "new test: "\
                    + str(calendar.timegm(d.utctimetuple()))\
                    + "\n"
        message = new_stamp + old_stamp
        agent.commit_changes_and_push(message)
        self.assertLess(int(old_stamp[-10:]), int(new_stamp[-10:]),
                msg="value on github should be updating")


