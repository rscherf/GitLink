# GitLink
Sublime Text plugin to derive URLS to files in your source repositories. No more traversing your file structure finding the file you are working on. With support for:
* <http://github.com>
* <http://bitbucket.org>
* <https://about.gitlab.com>
* <http://codebasehq.com>

Written by Ryan Scherf : <http://ryan.sc> - <http://twitter.com/ryanscherf>
* CodebaseHQ support by <http://iRonin.pl>
* GitLab support by <https://github.com/mbobin>

## How it works

![Right click in side menu](http://f.cl.ly/items/1O100K122E0a1x0y3V1k/Screen%20Shot%202014-10-20%20at%209.46.38%20AM.png)
![Right click in a file](http://f.cl.ly/items/3f1r0h0q1t2J003M2W0A/Screen%20Shot%202014-10-20%20at%209.46.24%20AM.png)

Or search for "GitLink" in the Command Palette

#### Copy URLs to files

`command + shift + c` Right click any file in the sidebar (that is part of a Git repository) and go to the `GitLink` menu item to see options.

#### Copy URLs to files with a deeplink the line number

Right click anywhere within the file you are currently editing. Your cursor position determines which line number will be used for the deeplink.

#### Open URLs in your default browser as a new tab

`command + shift + o` Use your default web browser (Chrome) to skip a step and open any of the links automatically in a new tab.

# Installation
The easiest is to install using [Package control](https://sublime.wbond.net/).

To install manually, you can clone Git repository directly:
* `cd ~/Library/Application Support/Sublime Text 2/Packages/`
* `git clone git@github.com:rscherf/GitLink.git`
* Restart Sublime Text

# Configuration
To switch to generating permanent links that reference a git commit hash instead of branch name, add `"gitlink_revision_type": "commithash"` to your Preferences.sublime-settings file.

# Contribute
GitHub and Sublime Text are powerful; I know all of you can make this way better than me.

1. Fork/clone the repository
2. Add whatever you'd like
3. Submit a Pull Request

# Copyright
1. Star the Github repository
2. Follow http://twitter.com/ryanscherf on Twitter and tell me how much you love this plugin
3. Use it however you'd like
