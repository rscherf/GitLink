import os
import re
import webbrowser
import sublime
import sublime_plugin
import subprocess

REMOTE_CONFIG = {
    'github': {
        'url': 'https://github.com/{0}/{1}/blob/{2}{3}/{4}',
        'line_param': '#L'
    },
    'bitbucket': {
        'url': 'https://bitbucket.org/{0}/{1}/src/{2}{3}/{4}',
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
        path, filename = os.path.split(self.view.file_name())

        # Switch to cwd of file
        os.chdir(path + "/")

        # Find the repo
        git_config_path = self.getoutput("git remote show origin")

        p = re.compile(r"(.+@)*([\w\d\.]+):(.*)")
        parts = p.findall(git_config_path)
        site_name = parts[0][1]  # github.com or bitbucket.org, whatever

        remote_name = 'github'
        if 'bitbucket' in site_name:
            remote_name = 'bitbucket'
        if 'codebasehq.com' in site_name:
            remote_name = 'codebasehq'
        remote = REMOTE_CONFIG[remote_name]

        git_config = parts[0][2]

        # Get username and repository
        if remote_name != 'codebasehq':
            user, repo = git_config.replace(".git", "").split("/")
        else:
           user, project, repo = git_config.replace(".git", "").split("/")

        # Find top level repo in current dir structure
        folder = self.getoutput("git rev-parse --show-toplevel")
        basename = os.path.basename(folder)
        remote_path = path.split(basename, 1)[1]

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
            os.system("echo '%s' | pbcopy" % url)
            sublime.status_message('GIT url has been copied to clipboard')
