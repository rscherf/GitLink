import os
import re
import webbrowser
import sublime
import sublime_plugin

# Backwards compatibility
try:
    import commands as cmd
except:
    import subprocess as cmd


REMOTE_CONFIG = {
    'github': {
        'url': 'https://github.com/{0}/{1}/blob/{2}{3}/{4}',
        'line_param': '#L'
    },
    'bitbucket': {
        'url': 'https://bitbucket.org/{0}/{1}/src/{2}{3}/{4}',
        'line_param': '#cl-'
    }
}


class GithublinkCommand(sublime_plugin.TextCommand):

    def run(self, edit, **args):
        # Current file path & filename
        path, filename = os.path.split(self.view.file_name())

        # Switch to cwd of file
        os.chdir(path + "/")

        # Find the repo
        git_config_path = cmd.getoutput("git remote show origin")

        p = re.compile(r"(.+@)*([\w\d\.]+):(.*)")
        parts = p.findall(git_config_path)
        site_name = parts[0][1]  # github.com or bitbucket.org, whatever
        git_config = parts[0][2]

        # Get Github username and repository
        user, repo = git_config.replace(".git", "").split("/")

        # Find top level repo in current dir structure
        basename = cmd.getoutput("basename `git rev-parse --show-toplevel`")
        remote_path = path.split(basename, 1)[1]

        # Find the current branch
        branch = cmd.getoutput("git rev-parse --abbrev-ref HEAD")

        remote_name = 'github'
        if 'bitbucket' in site_name:
            remote_name = 'bitbucket'

        remote = REMOTE_CONFIG[remote_name]

        # Build the URL
        url = remote['url'].format(user, repo, branch, remote_path, filename)

        if(args['line']):
            row = self.view.rowcol(self.view.sel()[0].begin())[0] + 1
            url += "{0}{1}".format(remote['line_param'], row)

        if(args['web']):
            webbrowser.open_new_tab(url)
        else:
            os.system("echo '%s' | pbcopy" % url)
            sublime.status_message('GIT url has been copied to clipboard')
