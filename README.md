**This repository is looking for a new maintainer**

# GitLink
Sublime Text plugin to derive shareable URLs to files in your source repositories. No more traversing your file structure finding the file you are working on. With support for:
* <https://github.com>
* <https://bitbucket.org>
* <https://about.gitlab.com>
* <https://codebasehq.com>
* <https://codeberg.org>
* <https://sr.ht>
* <https://gitea.com>

## How it works

![Right click in side menu](http://f.cl.ly/items/1O100K122E0a1x0y3V1k/Screen%20Shot%202014-10-20%20at%209.46.38%20AM.png)  
![Right click in a file](http://f.cl.ly/items/3f1r0h0q1t2J003M2W0A/Screen%20Shot%202014-10-20%20at%209.46.24%20AM.png)

Or search for "GitLink" in the Command Palette

### Copy URLs to files

Right click any Git-tracked file in the sidebar and go to the **GitLink** menu item to see options or <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>C</kbd> to copy the URL for the current file (<kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>C</kbd> on MacOS).

### Copy URLs to files with a deeplink to the line number

Right click anywhere within the file you are currently editing. Your cursor position determines which line number will be used for the deeplink.

### Open URLs in your default browser as a new tab

<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>O</kbd> Use your default web browser to skip a step and open any of the links automatically in a new tab(<kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>O</kbd> on MacOS).

## Installation
The easiest way is to install using [Package Control](https://packagecontrol.io).

To install manually, you can clone the Git repository directly:
* Mac:
  * `cd ~/Library/Application Support/Sublime Text/Packages/`
* Linux:
  * `cd ~/.config/sublime-text/Packages`
* `git clone git@github.com:rscherf/GitLink.git`
* Restart Sublime Text

## Configuration
To switch to generating permanent links that reference a git commit hash instead of branch name, add `"gitlink_revision_type": "commithash"` to your Preferences.sublime-settings file.

## Contribute
GitHub and Sublime Text are powerful; I know all of you can make this way better than me.

1. Fork/clone the repository
1. Add whatever you'd like
1. Submit a Pull Request

## Copyright
1. Star the Github repository
1. Follow http://twitter.com/ryanscherf on Twitter and tell me how much you love this plugin
1. Use it however you'd like
