import os
import re
import webbrowser
import sublime
import sublime_plugin
import subprocess

HOSTINGS = {
    'github': {
        'url': 'https://github.com/{user}/{repo}/blob/{revision}/{remote_path}{filename}',
        'blame_url': 'https://github.com/{user}/{repo}/blame/{revision}/{remote_path}{filename}',
        'line_param': '#L',
        'line_param_sep': '-L'
    },
    'bitbucket': {
        'url': 'https://bitbucket.org/{user}/{repo}/src/{revision}/{remote_path}{filename}',
        'blame_url': 'https://bitbucket.org/{user}/{repo}/annotate/{revision}/{remote_path}{filename}',
        'line_param': '#cl-',
        'line_param_sep': ':'
    },
    'gitlab': {
        'url': 'https://{domain}/{user}/{repo}/-/blob/{revision}/{remote_path}{filename}',
        'blame_url': 'https://{domain}/{user}/{repo}/-/blame/{revision}/{remote_path}{filename}',
        'line_param': '#L',
        'line_param_sep': '-'
    }
}

REMOTE_URL_PATTERN = re.compile(r"Fetch URL: [\w\d\.]+[:|@]/?/?(.*)")

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

        # Find the remote
        remote_name = self.getoutput("git remote show | grep upstream || echo origin")
        fetch_url = self.getoutput(f"git remote show {remote_name} -n | grep 'Fetch URL: '")
        # Determine git URL which may be either HTTPS or SSH form
        # (i.e. https://domain/user/repo or git@domain:user/repo)
        #
        # 'remote' would be 'domain/user/repo' or 'domain:user/repo'
        remote = REMOTE_URL_PATTERN.search(fetch_url).group(1)
        remote = re.sub('.git$', '', remote)

        for hosting_name, hosting in HOSTINGS.items():
            if hosting_name in remote:
                break

        # Get username and repository
        if ':' in remote:
            # SSH repository
            # format is {domain}:{user}/{repo}.git
            domain, user, repo = remote.replace(":", "/").split("/")
        else:
            # HTTP repository
            # format is {domain}/{user}/{repo}.git
            domain, user, repo = remote.split("/")

        # Find top level repo in current dir structure
        remote_path = self.getoutput("git rev-parse --show-prefix")

        # Find the current revision
        revision = self.getoutput("git rev-parse HEAD")

        # Choose the view type we'll use
        if 'blame' in args and args['blame']:
            view_type = 'blame_url'
        else:
            view_type = 'url'

        # Build the URL
        url = hosting[view_type].format(domain=domain, user=user, repo=repo, revision=revision, remote_path=remote_path, filename=filename)

        if args['line']:
            region = self.view.sel()[0]
            first_line = self.view.rowcol(region.begin())[0] + 1
            last_line = self.view.rowcol(region.end())[0] + 1
            if first_line == last_line:
                url += "{0}{1}".format(hosting['line_param'], first_line)
            else:
                url += "{0}{1}{2}{3}".format(hosting['line_param'], first_line, hosting['line_param_sep'], last_line)

        if args['web']:
            webbrowser.open_new_tab(url)
        else:
            sublime.set_clipboard(url)
            sublime.status_message('Git URL has been copied to clipboard')
