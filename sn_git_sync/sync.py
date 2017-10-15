# coding: utf-8
# %load sync.py
import simplenote
import sh
import os
import getpass
import sys
import readline
from pathlib import Path

class SnGitSync:
    local_path = os.path.join(os.path.sep, str(Path.home()), ".sngit")
    notes_path = os.path.join(os.path.sep, local_path ,  "notes")
    git = sh.git.bake(_cwd=notes_path)

    def __init__(self, repo_url):
        self.repo_url = repo_url

        if not os.path.exists(SnGitSync.local_path):
            try:
                os.makedirs(SnGitSync.local_path)

                with open(os.path.join(os.path.sep, SnGitSync.local_path, "repo"),
                          'w') as file:
                    file.write(repo_url)
                    file.close()

                if not os.path.exists(SnGitSync.notes_path):
                    os.makedirs(SnGitSync.notes_path)
                    SnGitSync.git.init()
            except Exception as ex:
                print(ex)
                print("rolling back changes")
                sh.rm("-rf", SnGitSync.local_path)



    def CheckConfig():
        return os.path.exists(SnGitSync.local_path)

    def ReadRepoStr():
        with open(os.path.join(os.path.sep, SnGitSync.local_path, "repo"),
                 'r') as file:
            return file.read()

    def PromptRepoStr():
        def default_hook():
            readline.insert_text("")
            readline.redisplay()

        def remote_hook():
            username = getpass.getuser()
            readline.insert_text("git@github.com:{}/notes.git"                                 .format(username))
            readline.redisplay()

        readline.set_pre_input_hook(remote_hook)
        repo_str = input("notes repo: ")
        readline.set_pre_input_hook(default_hook)
        return repo_str

def main():
    if not SnGitSync.CheckConfig():
        if len(sys.argv) > 1:
            sngs = SnGitSync(argv[1])
        else:
            sngs = SnGitSync(SnGitSync.PromptRepoStr())
    else:
        sngs = SnGitSync(SnGitSync.ReadRepoStr())

if __name__ == '__main__':
    main()
