import sys, os, re, webbrowser, sublime, sublime_plugin

# Backwards compatibility
try:
  import commands as cmd
except:
  import subprocess as cmd

class GitlinkCommand(sublime_plugin.TextCommand):
  def run(self, edit, **args):
    # Current file path & filename
    path, filename = os.path.split(self.view.file_name())

    # Switch to cwd of file
    os.chdir(path + "/")

    # Find the repo
    git_config_path = cmd.getoutput("git remote show origin")

    p = re.compile(r"(.+@)*([\w\d\.]+):(.*)")
    git_config = p.findall(git_config_path)[0][2]

    # Get Github username and repository
    user, repo = git_config.replace(".git", "").split("/")

    # Find top level repo in current dir structure
    basename = cmd.getoutput("basename `git rev-parse --show-toplevel`")
    remote_path = path.split(basename)[1]

    # Find the current branch
    branch = cmd.getoutput("git rev-parse --abbrev-ref HEAD")

    # Build the URL
    url = "https://github.com/{0}/{1}/blob/{2}{3}/{4}".format(user, repo, branch, remote_path, filename)

    if(args['line']):
      row =  self.view.rowcol(self.view.sel()[0].begin())[0] + 1
      url += "#L{0}".format(row)

    if(args['web']):
      webbrowser.open_new_tab(url)
      print "Opened '" + url + "' in a new tab."
    else:
      print "Copied '" + url + "' to clipboard."
      os.system("echo '%s' | pbcopy" % url)


