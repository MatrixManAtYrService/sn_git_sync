import simplenote
import sh
import os
import getpass
import sys
import readline
import argparse
from pathlib import Path
from sn_git.git import Agent as GitAgent
from sn_git.cmd import Parser as SngitParser

config_dir = os.path.join(os.path.sep, str(Path.home()), ".sngit")

def on_config(args):
    print("config", args.__dict__)
#    agent = GitAgent(config_dir, args.repo_name, args.repo_url)

def on_sync(args):
    print("sync", args.__dict__)


def main():

    parser = SngitParser(sys.argv[0], config_dir, on_config, on_sync)

    if len(sys.argv) == 1:
        parser.parse([''])
    else:
        parser.parse(sys.argv[1:])

#        if args.repo:
#            agent = Agent(args.repo)
#        else:
#            if not Agent.CheckConfig():
#                agent = Agent(Agent.PromptRepoStr())
#            else:
#                agent = Agent(Agent.ReadRepoStr())

if __name__ == '__main__':
    main()
