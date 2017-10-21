import argparse
import sys

# based on https://docs.python.org/3/library/argparse.html#action
class HelpAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not Allowed")
        super(HelpAction, self).__init__(option_strings, dest, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

        try:
            self.commands[namespace.command].parse_args(['--help'])
        except KeyError:
            print("{} is not a valid command".format(namespace.command))


class Parser:

    def __init__(self, command, config_dir, config_callback, sync_callback):
        self.command = command
        self.config_dir = config_dir
        self.config_callback = config_callback
        self.sync_callback = sync_callback

        # top-level
        self.parser = argparse.ArgumentParser(
                    prog=command,
                    description="a two-way sync between simplenote and git",
                    usage="{} <command> <args>".format(sys.argv[0]))

        self.subparsers = self.parser.add_subparsers()
        self._config_sub()
        self._sync_sub()
        self._help_sub()


    def _config_sub(self):
        parser_config = self.subparsers.add_parser(
            'configure',
            usage='configure <repo_name> <repo_url>',
            help='create or modify a repo entry in {}'
                    .format(self.config_dir))

        parser_config.add_argument(
            'repo_name',
            help="a local name for this repo")

        parser_config.add_argument('repo_url',
            help="something like git@github.com:fooUser/barRepo.git")

        parser_config.set_defaults(func=self.config_callback)

    def _sync_sub(self):
        parser_sync = self.subparsers.add_parser(
            'sync',
            usage='sync <simplenote user> <simplenote password> [repo_name]',
            help='sync symplenote with git')

        parser_sync.add_argument(
            'sn_user',
            help="the simplenote username")

        parser_sync.add_argument(
            'sn_pass',
            help="the simplenote password")

        parser_sync.add_argument(
            '-r', '--repo',
            help="sync only the specified repo")

        parser_sync.set_defaults(func=self.sync_callback)


    def _help_sub(self):

        parser_help = self.subparsers.add_parser(
                'help',
                usage='help <command>',
                help='display help for the specified command')

        HelpAction.commands = self.subparsers.choices

        parser_help.add_argument(
            'command',
            action=HelpAction,
            help="the command you want help with")


    def parse(self, args_list):
        args = self.parser.parse_args(args_list)
        args.func(args)

