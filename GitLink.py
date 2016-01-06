import os
import re
import webbrowser
import sublime
import sublime_plugin
import subprocess

REMOTE_CONFIG = {
    'github': {
        'url': 'https://github.com/{0}/{1}/blob/{2}/{3}{4}',
        'line_param': '#L'
    },
    'bitbucket': {
        'url': 'https://bitbucket.org/{0}/{1}/src/{2}/{3}{4}',
        'line_param': '#cl-'
    },
    'codebasehq': {
        'url': 'https://{0}.codebasehq.com/projects/{1}/repositories/{2}/blob/{3}{4}/{5}',
        'line_param': '#L'
    }
}


class GitlinkCommand(sublime_plugin.TextCommand):

    def getoutput(self, command):
        out, err = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()
        return out.decode().strip()

    def run(self, edit, **args):
        # Current file path & filename

        # only works on current open file
        path, filename = os.path.split(self.view.file_name())

        # Switch to cwd of file
        os.chdir(path + "/")

        # Find the repo
        git_config_path = self.getoutput("git remote show origin -n")

        # Determine git URL which may be either HTTPS or SSH form
        # (i.e. https://domain/user/repo or git@domain:user/repo)
        #
        # parts[0][2] will contain 'domain/user/repo' or 'domain:user/repo'
        #
        # see https://regex101.com/r/pZ3tN3/2 & https://regex101.com/r/iS5tQ4/2
        p = re.compile(r"(.+: )*([\w\d\.]+)[:|@]/?/?(.*)")
        parts = p.findall(git_config_path)
        git_config = parts[0][2]

        remote_name = 'github'
        if 'bitbucket' in git_config:
            remote_name = 'bitbucket'
        if 'codebasehq.com' in git_config:
            remote_name = 'codebasehq'
        remote = REMOTE_CONFIG[remote_name]


        # need to get username from full url

        # Get username and repository
        if remote_name != 'codebasehq':
            source, user, repo = git_config.replace(".git", "").replace("https://", "").split("/")
        else:
           user, project, repo = git_config.replace(".git", "").replace("https://", "").split("/")

        # Find top level repo in current dir structure
        remote_path = self.getoutput("git rev-parse --show-prefix")

        # Find the current branch
        branch = self.getoutput("git rev-parse --abbrev-ref HEAD")

        # Build the URL
        if remote_name != 'codebasehq':
            url = remote['url'].format(user, repo, branch, remote_path, filename)
        else:
            url = remote['url'].format(user, project, repo, branch, remote_path, filename)

        if(args['line']):
            row = self.view.rowcol(self.view.sel()[0].begin())[0] + 1
            url += "{0}{1}".format(remote['line_param'], row)

        if(args['web']):
            webbrowser.open_new_tab(url)
        else:
            sublime.set_clipboard(url)
            sublime.status_message('GIT url has been copied to clipboard')