# GitLink

Sublime Text plugin to derive shareable URLs
to files in your source repositories.
No more traversing your file structure
to find the file you are working on.
With support for:

* [GitHub][]
* [Bitbucket][]
* [GitLab][]
* [Codebase][]
* [Forgejo][] / [Codeberg][]
* [Sourcehut][]
* [Gitea][]
* [Gitee][]
* [CGit][]


## How it works

![Right click in side menu](http://f.cl.ly/items/1O100K122E0a1x0y3V1k/Screen%20Shot%202014-10-20%20at%209.46.38%20AM.png)  
![Right click in a file](http://f.cl.ly/items/3f1r0h0q1t2J003M2W0A/Screen%20Shot%202014-10-20%20at%209.46.24%20AM.png)

Or search for "GitLink" in the Command Palette.


### Copy URLs to files

Right click any Git-tracked file in the sidebar
and go to the **GitLink** menu item to see options,
or <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>C</kbd>
to copy the URL for the current file
(<kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>C</kbd> on MacOS).


### Copy URLs to files with a deeplink to the line number

Right click anywhere within the file you are currently editing.
Your cursor position determines which line number
will be used for the deeplink.


### Open URLs in your default browser as a new tab

<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>O</kbd>
to skip a step and open any of the links
in a new tab of your default web browser
(<kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>O</kbd> on MacOS).


## Installation

The easiest way is to install is using [Package Control][pc].

To install manually, you can clone the Git repository directly:
* Mac:
  * `cd ~/Library/Application Support/Sublime Text/Packages/`
* Linux:
  * `cd ~/.config/sublime-text/Packages`
* `git clone git@github.com:rscherf/GitLink.git`
* Restart Sublime Text


## Configuration

Things work out of the box for several Git hosts.
To customize further,
use the **Preferences: GitLink Settings** command
to open the settings.
Defaults are on the left,
and your changes are on the right.

### Repo matching

If you self-host a Git provider,
you can link your domain to its format
with `"user_repo_lookup"`:
Make a map of (JSON-escaped) domain-matching regular expressions
to the ID of the Git software your server runs.

If you need to create a new Git provider,
first consider making a PR here.
Otherwise, use `"user_repo_hosts"`
and follow the sample in the settings file,
or copy and modify one
from the defaults below it.

### Link format

To switch to generating permanent links
that reference a Git commit hash instead of branch name,
set `"revision_type": "commithash"`.
Commits not pushed to the server will 404.


## Contribute

Git and Sublime Text are powerful;
I know all of you can make this way better than me.

1. Fork/clone the repository.
1. Add whatever you'd like.
1. Run tests with the [UnitTesting][] package.
1. Submit a Pull Request.


## Copyright

1. Star the Github repository.
1. Follow [ryanscherf][twitter] on Twitter,
   and tell me how much you love this plugin.
1. Use it however you'd like.


[github]: https://github.com
[bitbucket]: https://bitbucket.org
[gitLab]: https://about.gitlab.com
[codebase]: https://codebasehq.com
[forgejo]: https://forgejo.org
[codeberg]: https://codeberg.org
[sourcehut]: https://sr.ht
[gitea]: https://gitea.com
[gitee]: https://gitee.com
[cgit]: https://git.zx2c4.com/cgit/about/

[pc]: https://packagecontrol.io
[unittesting]: https://packagecontrol.io/packages/UnitTesting
[twitter]: https://twitter.com/ryanscherf
