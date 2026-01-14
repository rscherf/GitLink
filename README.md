# GitLink

It's a Sublime Text plugin for shareable URLs
to files in your source repositories.
No more traversing your file structure
to find the file you are working on.
With support for
[GitHub][],
[Bitbucket][],
[GitLab][],
and many more.
See [the full list][support]
or [configure your own][configuration].


## How it works

| Sidebar | File content |
|:-:|:-:|
|![Right click in the sidebar][sidebar-menu]|![Right click in a file][context-menu]|

Or search for "GitLink" in the Command Palette
<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>
(<kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> on MacOS).


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
If supported by the Git service provider,
you can select multiple lines
to deeplink the line range.


### Open URLs in your default browser as a new tab

<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>O</kbd>
to skip a step and open any of the links
in a new tab of your default web browser
(<kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>O</kbd> on MacOS).


## Installation

The easiest way is to install is using [Package Control][pc].
Search for **GitLink** in the PC client plugin and install.

To install manually,
clone or symlink `https://github.com/rscherf/GitLink.git`
(or your fork)
into the Sublime Text `Packages` folder:
+ Mac: `~/Library/Application Support/Sublime Text/Packages`
+ Linux: `~/.config/sublime-text/Packages`
+ Windows: `%APPDATA%\Sublime Text\Packages`


## Git service provider support

Repository hosts are listed alphabetically.

### Upon install

[Arch Linux][][^gitlab],
[Assembla][],
[Bitbucket][],
[Codebase][],
[Codeberg][][^forgejo],
Debian [Salsa][][^gitlab],
[Eclipse][][^gitlab],
[GitHub][],
[GitLab][],
[Gitea][],
[Gitee][],
[GNOME][][^gitlab],
GNU [Savannah][][^cgit],
[Gogs][],
[Launchpad][][^cgit],
[Kernel.org][][^cgit],
[KDE][][^gitlab],
Fedora [Pagure][],
[Phabricator][],
[Phorge][],
[Radicle][],
[RhodeCode][],
[Sourcehut][],
[SourceForge][][^sourceforge],
[Tangled][],
and
[TuxFamily][][^cgit]

### With domain configuration

Any of the above plus
[CGit][],
[Gerrit][],
[GitWeb][] (which comes with Git),
and
[Forgejo][]

If you have a supported host
with their host ID in the hostname,
no configuration is required:
e.g. `gitlab.example.com`.

### With full configuration

Any site you want.
Please open an issue or PR
if it would help others.


## Configuration

Things work out of the box for many Git hosts.
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

1. Fork / clone the repository.
1. Add whatever you'd like.
1. Run tests with the [UnitTesting][] package.
1. Submit a Pull Request.


## Copyright

1. Star the Github repository.
1. Follow [@ryanscherf][twitter] on Twitter,
   and tell me how much you love this plugin.
1. Use it however you'd like.


[^cgit]: Linked to `cgit`  
[^forgejo]: Linked to `forgejo`  
[^gitlab]: Linked to `gitlab`  
[^sourceforge]: [SourceForge][] does not support blame or line numbers.  


[support]: https://github.com/rscherf/GitLink#git-service-provider-support
[configuration]: https://github.com/rscherf/GitLink#configuration

[arch linux]: https://gitlab.archlinux.org
[assembla]: https://get.assembla.com
[bitbucket]: https://bitbucket.org
[cgit]: https://git.zx2c4.com/cgit/about/
[codebase]: https://codebasehq.com
[codeberg]: https://codeberg.org
[eclipse]: https://www.eclipse.org
[forgejo]: https://forgejo.org
[gerrit]: https://www.gerritcodereview.com
[gitea]: https://gitea.com
[gitee]: https://gitee.com
[github]: https://github.com
[gitlab]: https://about.gitlab.com
[gitweb]: https://git-scm.com/book/en/v2/Git-on-the-Server-GitWeb
[gnome]: https://gitlab.gnome.org
[gogs]: https://gogs.io
[kde]: https://invent.kde.org
[kernel.org]: https://kernel.org
[launchpad]: https://code.launchpad.net
[pagure]: https://pagure.io
[phabricator]: https://phacility.com/phabricator
[phorge]: https://we.phorge.it
[radicle]: https://radicle.xyz
[rhodecode]: https://rhodecode.com
[salsa]: https://salsa.debian.org
[savannah]: https://savannah.gnu.org
[sourceforge]: https://sourceforge.net
[sourcehut]: https://sr.ht
[tangled]: https://tangled.org
[tuxfamily]: https://www.tuxfamily.org

[sidebar-menu]: demo/sidebar-menu.png
[context-menu]: demo/context-menu.png

[pc]: https://packagecontrol.io
[unittesting]: https://packagecontrol.io/packages/UnitTesting
[twitter]: https://twitter.com/ryanscherf
