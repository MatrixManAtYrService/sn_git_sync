import sh
import pysed
import re
import os
import getpass
import sys
import readline
import argparse
from collections import namedtuple
from pathlib import Path
from enum import Enum

class Agent:

    def configure_repo(self):

        # create directory if not exists
        if not os.path.exists(self.repo_dir):
            try:
                os.makedirs(self.repo_dir)

            except Exception as ex:
                print(ex)
                print("rolling back changes")
                sh.rm("-rf", self.repo_dir)
                raise ex

        if not os.path.exists(os.path.join(os.path.sep, self.repo_dir, '.git')):
            self.git.init()

        # add/modify remotes
        ConfiguredRemote = namedtuple('ConfiguredRemote', 'name url')

        configured_remotes = []
        remote_list_item = re.compile('([a-zA-Z0-9]*)\s*([^ ].*)\s*\(')
        for line in str(self.git.remote(verbose=True).stdout, 'utf-8').split('\n'):
            matches = remote_list_item.search(line)
            if (matches):
                configured_remotes.append(ConfiguredRemote(matches.groups()[0],
                                                           matches.groups()[1]))

        remote_exists = False
        remote_matches = False
        for remote in configured_remotes:
            if remote.name is self.remote_name:
                remote_exists = True
                if remote.url is self.remote_url:
                    remote_matches = True

        if remote_exists and not remote_matches:
            self.git.remote('remove', self.remote_name)
            self.git.remote('add', self.remote_name, self.remote_url)
        else:
            self.git.remote('add', self.remote_name, self.remote_url)

        # update repo
        self.git.pull(self.remote_name, 'master')

    def commit_changes_and_push(self, message):
        self.git.add('-A')
        self.git.commit(['-m', message])
        self.git.push([self.remote_name, 'master'])


    def __init__(self, config_dir, repo_name, repo_url):
        self.config_dir = config_dir
        self.remote_url = repo_url
        self.repo_name = repo_name
        self.remote_name = repo_name + "_sngit"
        self.repo_dir= os.path.join(os.path.sep, config_dir, repo_name)
        self.repo_hook = os.path.join(os.path.sep, self.repo_dir + ".py")
        self.git = sh.git.bake(_cwd=self.repo_dir)


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
