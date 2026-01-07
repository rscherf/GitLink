import os
import re
import webbrowser
import sublime
import subprocess
from sublime_plugin import TextCommand
from .RepositoryParser import RepositoryParser


class GitlinkCommand(TextCommand):
    cwd = os.getcwd()

    def getoutput(self, args, fallback=None, cwd=None, **kwargs):
        working_dir = cwd if cwd else self.cwd
        proc = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=working_dir, **kwargs
        )
        out, err = proc.communicate()
        return_code = proc.returncode
        if return_code != 0:
            if fallback:
                return fallback

            raise RuntimeError("Failed to run: '{}' (code:{}) with error: {}".format(
                args, return_code, err.decode().strip())
            )
        return out.decode().strip()

    def lookup_ssh_host(self, hostname, config_file=None):
        ssh_args = ['ssh', '-G', hostname]
        if config_file:
            ssh_args += ['-F', config_file]
        ssh_output = self.getoutput(ssh_args, 'hostname ' + hostname)
        match = re.search(r'hostname (.*)', ssh_output, re.MULTILINE)
        return match.group(1) if match else hostname

    def is_enabled(self):
        try:
            self.cwd, _ = os.path.split(self.view.file_name())
            self.getoutput(['git', 'rev-parse', 'HEAD'])
            return True
        except:
            return False

    def run(self, edit, **args):
        # Current file path & filename

        # only works on current open file
        self.cwd, filename = os.path.split(self.view.file_name())

        # Find the current revision
        settings = sublime.load_settings('GitLink.sublime-settings')
        rev_type = settings.get('revision_type')
        if rev_type == 'commithash':
            revision = self.getoutput(['git', 'rev-parse', 'HEAD'])
        elif rev_type == 'abbrev':
            revision = self.getoutput(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        else:
            raise NotImplementedError('Unknown ref setting: ' + rev_type)

        # Find the remote of the current branch
        branch_name = self.getoutput(['git', 'symbolic-ref', '--short', 'HEAD'])
        remote_name = self.getoutput(
            ['git', 'config', '--get branch.{}.remote'.format(branch_name)],
            fallback='origin')
        remote = self.getoutput(['git', 'remote', 'get-url', remote_name])
        repo = RepositoryParser(remote, rev_type)

        if 'ssh' in repo.scheme:
            # `domain` may be an alias configured in ssh
            repo.domain = self.lookup_ssh_host(repo.domain)

        # Find top level repo in current dir structure
        remote_path = self.getoutput(['git', 'rev-parse', '--show-prefix'])
        file = remote_path + filename

        if args['line']:
            region = self.view.sel()[0]
            first_line = self.view.rowcol(region.begin())[0] + 1
            last_line = self.view.rowcol(region.end())[0] + 1
        else:
            first_line = 0
            last_line = 0

        # Choose the view type we'll use
        if 'blame' in args and args['blame']:
            url = repo.get_blame_url(file, revision, first_line, last_line)
        else:
            url = repo.get_source_url(file, revision, first_line, last_line)

        if args['web']:
            webbrowser.open_new_tab(url)
        else:
            sublime.set_clipboard(url)
            sublime.status_message('Git URL has been copied to clipboard')
