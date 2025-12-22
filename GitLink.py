import os
import re
import webbrowser
import sublime
import sublime_plugin
import subprocess
from .gitlink.RepositoryParser import RepositoryParser


class GitlinkCommand(sublime_plugin.TextCommand):
    cwd = os.getcwd()

    def getoutput(self, command, fallback=None, cwd=None, **kwargs):
        working_dir = cwd if cwd else self.cwd
        proc = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
            cwd=working_dir, **kwargs
        )
        out, err = proc.communicate()
        return_code = proc.returncode
        if return_code != 0:
            if fallback:
                return fallback

            raise RuntimeError("Failed to run: '{}' (code:{}) with error: {}".format(
                command, return_code, err.decode().strip())
            )
        return out.decode().strip()

    def run(self, edit, **args):
        # Current file path & filename

        # only works on current open file
        self.cwd, filename = os.path.split(self.view.file_name())

        # Find the current revision
        settings = sublime.load_settings("Preferences.sublime-settings")
        ref_type = settings.get('gitlink_revision_type', 'abbrev')
        if ref_type == 'commithash':
            revision = self.getoutput("git rev-parse HEAD")
        elif ref_type == 'abbrev':
            revision = self.getoutput("git rev-parse --abbrev-ref HEAD")
        else:
            raise NotImplementedError('Unknown ref setting: ' + ref_type)

        # Find the remote of the current branch
        branch_name = self.getoutput("git symbolic-ref --short HEAD")
        remote_name = self.getoutput(
            "git config --get branch.{}.remote".format(branch_name), 'origin'
        )
        remote = self.getoutput("git remote get-url {}".format(remote_name))
        repo = RepositoryParser(remote, ref_type)

        if 'ssh' in repo.scheme:
            # `domain` may be an alias configured in ssh
            try:
                ssh_output = self.getoutput("ssh -G " + repo.domain)
            except:  # noqa intended unconditional except
                pass
            else:
                match = re.search(r'hostname (.*)', ssh_output, re.MULTILINE)
                repo.domain = match.group(1) if match else repo.domain

        # Find top level repo in current dir structure
        remote_path = self.getoutput("git rev-parse --show-prefix")
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
