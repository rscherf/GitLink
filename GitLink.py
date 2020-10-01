import os
import re
import webbrowser
import sublime
import sublime_plugin
import subprocess

REMOTE_CONFIG = {
    'github': {
        'url': 'https://github.com/{0}/{1}/blob/{2}/{3}{4}',
        'blame_url': 'https://github.com/{0}/{1}/blame/{2}/{3}{4}',
        'line_param': '#L',
        'line_param_sep': ':'
    },
    'bitbucket': {
        'url': 'https://bitbucket.org/{0}/{1}/src/{2}/{3}{4}',
        'blame_url': 'https://bitbucket.org/{0}/{1}/annotate/{2}/{3}{4}',
        'line_param': '#cl-',
        'line_param_sep': ':'
    },
    'codebasehq': {
        'url': 'https://{0}.codebasehq.com/projects/{1}/repositories/{2}/blob/{3}{4}/{5}',
        'blame_url': 'https://{0}.codebasehq.com/projects/{1}/repositories/{2}/blame/{3}{4}/{5}',
        'line_param': '#L',
        'line_param_sep': ':'
    },
    'gitlab': {
        'url': 'https://{0}/{1}/{2}/-/blob/{3}/{4}{5}',
        'blame_url': 'https://{0}/{1}/{2}/-/blame/{3}/{4}{5}',
        'line_param': '#L',
        'line_param_sep': '-'
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
        if 'gitlab' in git_config:
            remote_name = 'gitlab'
        remote = REMOTE_CONFIG[remote_name]


        # need to get username from full url

        # Get username and repository (& also project for codebasehq)
        remote_without_git = re.sub('.git$', '', git_config)
        if ':' in git_config:
            # SSH repository
            if remote_name == 'codebasehq':
                # format is codebasehq.com:{user}/{project}/{repo}.git
                domain, user, project, repo = remote_without_git.replace(":", "/").split("/")
            else:
                # format is {domain}:{user}/{repo}.git
                domain, user, repo = remote_without_git.replace(":", "/").split("/")
        else:
            # HTTP repository
            if remote_name == 'codebasehq':
                # format is {user}.codebasehq.com/{project}/{repo}.git
                domain, project, repo = remote_without_git.split("/")
                user = domain.split('.', 1)[0] # user is first segment of domain
            else:
                # format is {domain}/{user}/{repo}.git
                domain, user, repo = remote_without_git.split("/")

        # Find top level repo in current dir structure
        remote_path = self.getoutput("git rev-parse --show-prefix")

        # Find the current revision
        rev_type = self.view.settings().get('gitlink_revision_type', 'branch')
        if rev_type == 'branch':
            git_rev = self.getoutput("git rev-parse --abbrev-ref HEAD")
        elif rev_type == 'commithash':
            git_rev = self.getoutput("git rev-parse HEAD")

        # Choose the view type we'll use
        if('blame' in args && args['blame']):
            view_type = 'blame_url'
        else:
            view_type = 'url'

        # Build the URL
        if remote_name == 'codebasehq':
            url = remote[view_type].format(user, project, repo, git_rev, remote_path, filename)
        elif remote_name == 'gitlab':
            url = remote[view_type].format(domain, user, repo, git_rev, remote_path, filename)
        else:
            url = remote[view_type].format(user, repo, git_rev, remote_path, filename)

        if(args['line']):
            region = self.view.sel()[0]
            first_line = self.view.rowcol(region.begin())[0] + 1
            last_line = self.view.rowcol(region.end())[0] + 1
            if first_line == last_line:
                url += "{0}{1}".format(remote['line_param'], first_line)
            else:
                url += "{0}{1}{2}{3}".format(remote['line_param'], first_line, remote['line_param_sep'], last_line)

        if(args['web']):
            webbrowser.open_new_tab(url)
        else:
            sublime.set_clipboard(url)
            sublime.status_message('GIT url has been copied to clipboard')
