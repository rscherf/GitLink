from unittest import TestCase
from ..gitlink.RepositoryParser import RepositoryParser


class RepoParserUnknown(TestCase):

    def test_ssh_unknown_repo(self):
        self.assertRaises(
            NotImplementedError,
            lambda: RepositoryParser('git@gitxx.com:user/repo.git'))

    def test_https_unknown_repo(self):
        self.assertRaises(
            NotImplementedError,
            lambda: RepositoryParser('https://gitxx.com:user/repo.git'))

    def test_ssh_unknown_rev_type(self):
        self.assertRaises(
            NotImplementedError,
            lambda: RepositoryParser('git@github.com:user/repo.git', 'foo'))

    def test_https_unknown_rev_type(self):
        self.assertRaises(
            NotImplementedError,
            lambda: RepositoryParser('https://github.com:user/repo.git', 'foo'))


class RepoParserAssembla(TestCase):

    def test_ssh(self):
        parse_result = RepositoryParser('git@git.assembla.com:open-docs-md.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('assembla.com', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual(None, parse_result.owner)
        self.assertEqual('open-docs-md', parse_result.repo_name)
        self.assertEqual('https://app.assembla.com/spaces/open-docs-md/git/source/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://app.assembla.com/spaces/open-docs-md/git/source/master/README.md#ln5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://app.assembla.com/spaces/open-docs-md/git/source/master/README.md#ln5',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://app.assembla.com/spaces/open-docs-md/git/source/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://app.assembla.com/spaces/open-docs-md/git/source/blame/master/README.md#ln5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://app.assembla.com/spaces/open-docs-md/git/source/blame/master/README.md#ln5',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https(self):
        parse_result = RepositoryParser('https://git.assembla.com/open-docs-md.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('assembla.com', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual(None, parse_result.owner)
        self.assertEqual('open-docs-md', parse_result.repo_name)
        self.assertEqual('https://app.assembla.com/spaces/open-docs-md/git/source/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://app.assembla.com/spaces/open-docs-md/git/source/master/README.md#ln5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://app.assembla.com/spaces/open-docs-md/git/source/master/README.md#ln5',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://app.assembla.com/spaces/open-docs-md/git/source/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://app.assembla.com/spaces/open-docs-md/git/source/blame/master/README.md#ln5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://app.assembla.com/spaces/open-docs-md/git/source/blame/master/README.md#ln5',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))


class RepoParserBitbucket(TestCase):

    def test_ssh(self):
        parse_result = RepositoryParser('git@bitbucket.org:user/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('bitbucket.org', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://bitbucket.org/user/repo/src/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://bitbucket.org/user/repo/src/master/README.md#cl-5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://bitbucket.org/user/repo/src/master/README.md#cl-5:7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://bitbucket.org/user/repo/annotate/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://bitbucket.org/user/repo/annotate/master/README.md#cl-5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://bitbucket.org/user/repo/annotate/master/README.md#cl-5:7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https(self):
        parse_result = RepositoryParser('https://me@bitbucket.org/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('bitbucket.org', parse_result.domain)
        self.assertEqual('me', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://bitbucket.org/user/repo/src/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://bitbucket.org/user/repo/src/master/README.md#cl-5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://bitbucket.org/user/repo/src/master/README.md#cl-5:7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://bitbucket.org/user/repo/annotate/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://bitbucket.org/user/repo/annotate/master/README.md#cl-5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://bitbucket.org/user/repo/annotate/master/README.md#cl-5:7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https_no_user(self):
        parse_result = RepositoryParser('https://bitbucket.org/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('bitbucket.org', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://bitbucket.org/user/repo/src/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://bitbucket.org/user/repo/src/master/README.md#cl-5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://bitbucket.org/user/repo/src/master/README.md#cl-5:7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://bitbucket.org/user/repo/annotate/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://bitbucket.org/user/repo/annotate/master/README.md#cl-5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://bitbucket.org/user/repo/annotate/master/README.md#cl-5:7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))


class RepoParserCGit(TestCase):

    def test_ssh_cgit(self):
        parse_result = RepositoryParser('git@cgit.example.com:project/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('cgit.example.com', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual(None, parse_result.owner)
        self.assertEqual('project', parse_result.project)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://cgit.example.com/project/repo.git/tree/README.md?id=master',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://cgit.example.com/project/repo.git/tree/README.md?id=master#n5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://cgit.example.com/project/repo.git/tree/README.md?id=master#n5',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://cgit.example.com/project/repo.git/blame/README.md?id=master',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://cgit.example.com/project/repo.git/blame/README.md?id=master#n5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://cgit.example.com/project/repo.git/blame/README.md?id=master#n5',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https_cgit(self):
        parse_result = RepositoryParser('https://cgit.example.com/project/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('cgit.example.com', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual(None, parse_result.owner)
        self.assertEqual('project', parse_result.project)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://cgit.example.com/project/repo.git/tree/README.md?id=master',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://cgit.example.com/project/repo.git/tree/README.md?id=master#n5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://cgit.example.com/project/repo.git/tree/README.md?id=master#n5',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://cgit.example.com/project/repo.git/blame/README.md?id=master',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://cgit.example.com/project/repo.git/blame/README.md?id=master#n5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://cgit.example.com/project/repo.git/blame/README.md?id=master#n5',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_git_kernelorg(self):
        parse_result = RepositoryParser('git://git.kernel.org/pub/scm/git/git.git')
        self.assertEqual('git', parse_result.scheme)
        self.assertEqual('git.kernel.org', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual(None, parse_result.owner)
        self.assertEqual('pub/scm/git', parse_result.project)
        self.assertEqual('git', parse_result.repo_name)
        self.assertEqual('https://git.kernel.org/pub/scm/git/git.git/tree/README.md?id=master',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://git.kernel.org/pub/scm/git/git.git/tree/README.md?id=master#n5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://git.kernel.org/pub/scm/git/git.git/tree/README.md?id=master#n5',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://git.kernel.org/pub/scm/git/git.git/blame/README.md?id=master',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://git.kernel.org/pub/scm/git/git.git/blame/README.md?id=master#n5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://git.kernel.org/pub/scm/git/git.git/blame/README.md?id=master#n5',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https_kernelorg(self):
        parse_result = RepositoryParser('https://git.kernel.org/pub/scm/git/git.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('git.kernel.org', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual(None, parse_result.owner)
        self.assertEqual('pub/scm/git', parse_result.project)
        self.assertEqual('git', parse_result.repo_name)
        self.assertEqual('https://git.kernel.org/pub/scm/git/git.git/tree/README.md?id=master',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://git.kernel.org/pub/scm/git/git.git/tree/README.md?id=master#n5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://git.kernel.org/pub/scm/git/git.git/tree/README.md?id=master#n5',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://git.kernel.org/pub/scm/git/git.git/blame/README.md?id=master',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://git.kernel.org/pub/scm/git/git.git/blame/README.md?id=master#n5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://git.kernel.org/pub/scm/git/git.git/blame/README.md?id=master#n5',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_git_savannah(self):
        parse_result = RepositoryParser('git://git.git.savannah.gnu.org/patch.git')
        self.assertEqual('git', parse_result.scheme)
        self.assertEqual('cgit.git.savannah.gnu.org', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual(None, parse_result.owner)
        self.assertEqual('cgit', parse_result.project)
        self.assertEqual('patch', parse_result.repo_name)
        self.assertEqual('https://cgit.git.savannah.gnu.org/cgit/patch.git/tree/README.md?id=master',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://cgit.git.savannah.gnu.org/cgit/patch.git/tree/README.md?id=master#n5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://cgit.git.savannah.gnu.org/cgit/patch.git/tree/README.md?id=master#n5',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://cgit.git.savannah.gnu.org/cgit/patch.git/blame/README.md?id=master',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://cgit.git.savannah.gnu.org/cgit/patch.git/blame/README.md?id=master#n5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://cgit.git.savannah.gnu.org/cgit/patch.git/blame/README.md?id=master#n5',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_ssh_savannah(self):
        parse_result = RepositoryParser('ssh://git.savannah.gnu.org/srv/git/patch.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('cgit.git.savannah.gnu.org', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual(None, parse_result.owner)
        self.assertEqual('cgit', parse_result.project)
        self.assertEqual('patch', parse_result.repo_name)
        self.assertEqual('https://cgit.git.savannah.gnu.org/cgit/patch.git/tree/README.md?id=master',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://cgit.git.savannah.gnu.org/cgit/patch.git/tree/README.md?id=master#n5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://cgit.git.savannah.gnu.org/cgit/patch.git/tree/README.md?id=master#n5',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://cgit.git.savannah.gnu.org/cgit/patch.git/blame/README.md?id=master',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://cgit.git.savannah.gnu.org/cgit/patch.git/blame/README.md?id=master#n5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://cgit.git.savannah.gnu.org/cgit/patch.git/blame/README.md?id=master#n5',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https_savannah(self):
        parse_result = RepositoryParser('https://https.git.savannah.gnu.org/git/patch.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('cgit.git.savannah.gnu.org', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual(None, parse_result.owner)
        self.assertEqual('cgit', parse_result.project)
        self.assertEqual('patch', parse_result.repo_name)
        self.assertEqual('https://cgit.git.savannah.gnu.org/cgit/patch.git/tree/README.md?id=master',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://cgit.git.savannah.gnu.org/cgit/patch.git/tree/README.md?id=master#n5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://cgit.git.savannah.gnu.org/cgit/patch.git/tree/README.md?id=master#n5',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://cgit.git.savannah.gnu.org/cgit/patch.git/blame/README.md?id=master',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://cgit.git.savannah.gnu.org/cgit/patch.git/blame/README.md?id=master#n5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://cgit.git.savannah.gnu.org/cgit/patch.git/blame/README.md?id=master#n5',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_ssh_tuxfamily(self):
        parse_result = RepositoryParser('ssh://user@git.tuxfamily.org/gitroot/project/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('git.tuxfamily.org', parse_result.domain)
        self.assertEqual('user', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual(None, parse_result.owner)
        self.assertEqual('project', parse_result.project)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://git.tuxfamily.org/project/repo.git/tree/README.md?id=master',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://git.tuxfamily.org/project/repo.git/tree/README.md?id=master#n5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://git.tuxfamily.org/project/repo.git/tree/README.md?id=master#n5',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://git.tuxfamily.org/project/repo.git/blame/README.md?id=master',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://git.tuxfamily.org/project/repo.git/blame/README.md?id=master#n5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://git.tuxfamily.org/project/repo.git/blame/README.md?id=master#n5',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_git_tuxfamily(self):
        parse_result = RepositoryParser('git://git.tuxfamily.org/gitroot/project/repo.git')
        self.assertEqual('git', parse_result.scheme)
        self.assertEqual('git.tuxfamily.org', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual(None, parse_result.owner)
        self.assertEqual('project', parse_result.project)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://git.tuxfamily.org/project/repo.git/tree/README.md?id=master',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://git.tuxfamily.org/project/repo.git/tree/README.md?id=master#n5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://git.tuxfamily.org/project/repo.git/tree/README.md?id=master#n5',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://git.tuxfamily.org/project/repo.git/blame/README.md?id=master',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://git.tuxfamily.org/project/repo.git/blame/README.md?id=master#n5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://git.tuxfamily.org/project/repo.git/blame/README.md?id=master#n5',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))


class RepoParserCodebase(TestCase):

    def test_ssh(self):
        parse_result = RepositoryParser('git@codebasehq.com:user/project/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('codebasehq.com', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('project', parse_result.project)
        self.assertEqual('https://user.codebasehq.com/projects/project/repositories/repo/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://user.codebasehq.com/projects/project/repositories/repo/blob/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://user.codebasehq.com/projects/project/repositories/repo/blob/master/README.md#L5:7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://user.codebasehq.com/projects/project/repositories/repo/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://user.codebasehq.com/projects/project/repositories/repo/blame/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://user.codebasehq.com/projects/project/repositories/repo/blame/master/README.md#L5:7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https(self):
        parse_result = RepositoryParser('https://user.codebasehq.com/project/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('codebasehq.com', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('project', parse_result.project)
        self.assertEqual('https://user.codebasehq.com/projects/project/repositories/repo/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://user.codebasehq.com/projects/project/repositories/repo/blob/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://user.codebasehq.com/projects/project/repositories/repo/blob/master/README.md#L5:7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://user.codebasehq.com/projects/project/repositories/repo/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://user.codebasehq.com/projects/project/repositories/repo/blame/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://user.codebasehq.com/projects/project/repositories/repo/blame/master/README.md#L5:7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))


class RepoParserCodeberg(TestCase):

    def test_ssh_branch(self):
        parse_result = RepositoryParser('git@codeberg.org:user/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('codeberg.org', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://codeberg.org/user/repo/src/branch/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://codeberg.org/user/repo/src/branch/master/README.md?display=source#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://codeberg.org/user/repo/src/branch/master/README.md?display=source#L5-L7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://codeberg.org/user/repo/blame/branch/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://codeberg.org/user/repo/blame/branch/master/README.md?display=source#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://codeberg.org/user/repo/blame/branch/master/README.md?display=source#L5-L7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https_branch(self):
        parse_result = RepositoryParser('https://codeberg.org/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('codeberg.org', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://codeberg.org/user/repo/src/branch/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://codeberg.org/user/repo/src/branch/master/README.md?display=source#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://codeberg.org/user/repo/src/branch/master/README.md?display=source#L5-L7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://codeberg.org/user/repo/blame/branch/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://codeberg.org/user/repo/blame/branch/master/README.md?display=source#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://codeberg.org/user/repo/blame/branch/master/README.md?display=source#L5-L7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_ssh_sha(self):
        parse_result = RepositoryParser('git@codeberg.org:user/repo.git', 'commithash')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('codeberg.org', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://codeberg.org/user/repo/src/commit/deadbeef/README.md',
                         parse_result.get_source_url('README.md', 'deadbeef'))
        self.assertEqual('https://codeberg.org/user/repo/src/commit/deadbeef/README.md?display=source#L5',
                         parse_result.get_source_url('README.md', 'deadbeef', 5))
        self.assertEqual('https://codeberg.org/user/repo/src/commit/deadbeef/README.md?display=source#L5-L7',
                         parse_result.get_source_url('README.md', 'deadbeef', 5, 7))
        self.assertEqual('https://codeberg.org/user/repo/blame/commit/deadbeef/README.md',
                         parse_result.get_blame_url('README.md', 'deadbeef'))
        self.assertEqual('https://codeberg.org/user/repo/blame/commit/deadbeef/README.md?display=source#L5',
                         parse_result.get_blame_url('README.md', 'deadbeef', 5))
        self.assertEqual('https://codeberg.org/user/repo/blame/commit/deadbeef/README.md?display=source#L5-L7',
                         parse_result.get_blame_url('README.md', 'deadbeef', 5, 7))

    def test_https_sha(self):
        parse_result = RepositoryParser('https://codeberg.org/user/repo.git', 'commithash')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('codeberg.org', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://codeberg.org/user/repo/src/commit/deadbeef/README.md',
                         parse_result.get_source_url('README.md', 'deadbeef'))
        self.assertEqual('https://codeberg.org/user/repo/src/commit/deadbeef/README.md?display=source#L5',
                         parse_result.get_source_url('README.md', 'deadbeef', 5))
        self.assertEqual('https://codeberg.org/user/repo/src/commit/deadbeef/README.md?display=source#L5-L7',
                         parse_result.get_source_url('README.md', 'deadbeef', 5, 7))
        self.assertEqual('https://codeberg.org/user/repo/blame/commit/deadbeef/README.md',
                         parse_result.get_blame_url('README.md', 'deadbeef'))
        self.assertEqual('https://codeberg.org/user/repo/blame/commit/deadbeef/README.md?display=source#L5',
                         parse_result.get_blame_url('README.md', 'deadbeef', 5))
        self.assertEqual('https://codeberg.org/user/repo/blame/commit/deadbeef/README.md?display=source#L5-L7',
                         parse_result.get_blame_url('README.md', 'deadbeef', 5, 7))


class RepoParserGerrit(TestCase):

    def test_ssh(self):
        parse_result = RepositoryParser('git@gerrit.example.com:user/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('gerrit.example.com', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gerrit.example.com/repo/+/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://gerrit.example.com/repo/+/master/README.md#5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://gerrit.example.com/repo/+/master/README.md#5',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://gerrit.example.com/repo/+blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://gerrit.example.com/repo/+blame/master/README.md#5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://gerrit.example.com/repo/+blame/master/README.md#5',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https(self):
        parse_result = RepositoryParser('https://gerrit.example.com/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('gerrit.example.com', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gerrit.example.com/repo/+/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://gerrit.example.com/repo/+/master/README.md#5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://gerrit.example.com/repo/+/master/README.md#5',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://gerrit.example.com/repo/+blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://gerrit.example.com/repo/+blame/master/README.md#5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://gerrit.example.com/repo/+blame/master/README.md#5',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))


class RepoParserGitea(TestCase):

    def test_ssh_branch(self):
        parse_result = RepositoryParser('git@gitea.com:user/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('gitea.com', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gitea.com/user/repo/src/branch/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://gitea.com/user/repo/src/branch/master/README.md?display=source#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://gitea.com/user/repo/src/branch/master/README.md?display=source#L5-L7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://gitea.com/user/repo/blame/branch/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://gitea.com/user/repo/blame/branch/master/README.md?display=source#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://gitea.com/user/repo/blame/branch/master/README.md?display=source#L5-L7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https_branch(self):
        parse_result = RepositoryParser('https://gitea.com/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('gitea.com', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gitea.com/user/repo/src/branch/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://gitea.com/user/repo/src/branch/master/README.md?display=source#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://gitea.com/user/repo/src/branch/master/README.md?display=source#L5-L7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://gitea.com/user/repo/blame/branch/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://gitea.com/user/repo/blame/branch/master/README.md?display=source#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://gitea.com/user/repo/blame/branch/master/README.md?display=source#L5-L7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_ssh_sha(self):
        parse_result = RepositoryParser('git@gitea.com:user/repo.git', 'commithash')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('gitea.com', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gitea.com/user/repo/src/commit/deadbeef/README.md',
                         parse_result.get_source_url('README.md', 'deadbeef'))
        self.assertEqual('https://gitea.com/user/repo/src/commit/deadbeef/README.md?display=source#L5',
                         parse_result.get_source_url('README.md', 'deadbeef', 5))
        self.assertEqual('https://gitea.com/user/repo/src/commit/deadbeef/README.md?display=source#L5-L7',
                         parse_result.get_source_url('README.md', 'deadbeef', 5, 7))
        self.assertEqual('https://gitea.com/user/repo/blame/commit/deadbeef/README.md',
                         parse_result.get_blame_url('README.md', 'deadbeef'))
        self.assertEqual('https://gitea.com/user/repo/blame/commit/deadbeef/README.md?display=source#L5',
                         parse_result.get_blame_url('README.md', 'deadbeef', 5))
        self.assertEqual('https://gitea.com/user/repo/blame/commit/deadbeef/README.md?display=source#L5-L7',
                         parse_result.get_blame_url('README.md', 'deadbeef', 5, 7))

    def test_https_sha(self):
        parse_result = RepositoryParser('https://gitea.com/user/repo.git', 'commithash')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('gitea.com', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gitea.com/user/repo/src/commit/deadbeef/README.md',
                         parse_result.get_source_url('README.md', 'deadbeef'))
        self.assertEqual('https://gitea.com/user/repo/src/commit/deadbeef/README.md?display=source#L5',
                         parse_result.get_source_url('README.md', 'deadbeef', 5))
        self.assertEqual('https://gitea.com/user/repo/src/commit/deadbeef/README.md?display=source#L5-L7',
                         parse_result.get_source_url('README.md', 'deadbeef', 5, 7))
        self.assertEqual('https://gitea.com/user/repo/blame/commit/deadbeef/README.md',
                         parse_result.get_blame_url('README.md', 'deadbeef'))
        self.assertEqual('https://gitea.com/user/repo/blame/commit/deadbeef/README.md?display=source#L5',
                         parse_result.get_blame_url('README.md', 'deadbeef', 5))
        self.assertEqual('https://gitea.com/user/repo/blame/commit/deadbeef/README.md?display=source#L5-L7',
                         parse_result.get_blame_url('README.md', 'deadbeef', 5, 7))


class RepoParserGitee(TestCase):

    def test_ssh(self):
        parse_result = RepositoryParser('git@gitee.com:user/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('gitee.com', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gitee.com/user/repo/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://gitee.com/user/repo/blob/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://gitee.com/user/repo/blob/master/README.md#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://gitee.com/user/repo/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://gitee.com/user/repo/blame/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://gitee.com/user/repo/blame/master/README.md#L5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https(self):
        parse_result = RepositoryParser('https://gitee.com/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('gitee.com', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gitee.com/user/repo/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://gitee.com/user/repo/blob/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://gitee.com/user/repo/blob/master/README.md#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://gitee.com/user/repo/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://gitee.com/user/repo/blame/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://gitee.com/user/repo/blame/master/README.md#L5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))


class RepoParserGitHub(TestCase):

    def test_ssh(self):
        parse_result = RepositoryParser('git@github.com:user/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('github.com', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://github.com/user/repo/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://github.com/user/repo/blob/master/README.md?plain=1#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blob/master/README.md?plain=1#L5-L7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md?plain=1#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md?plain=1#L5-L7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_ssh_with_scheme(self):
        parse_result = RepositoryParser('ssh://git@github.com:user/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('github.com', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://github.com/user/repo/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://github.com/user/repo/blob/master/README.md?plain=1#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blob/master/README.md?plain=1#L5-L7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md?plain=1#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md?plain=1#L5-L7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https(self):
        parse_result = RepositoryParser('https://github.com/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('github.com', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://github.com/user/repo/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://github.com/user/repo/blob/master/README.md?plain=1#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blob/master/README.md?plain=1#L5-L7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md?plain=1#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md?plain=1#L5-L7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https_basicauth(self):
        parse_result = RepositoryParser('https://me@github.com/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('github.com', parse_result.domain)
        self.assertEqual('me', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://github.com/user/repo/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://github.com/user/repo/blob/master/README.md?plain=1#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blob/master/README.md?plain=1#L5-L7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md?plain=1#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md?plain=1#L5-L7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https_basicauth_pw(self):
        parse_result = RepositoryParser('https://me:password@github.com/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('github.com', parse_result.domain)
        self.assertEqual('me', parse_result.logon_user)
        self.assertEqual('password', parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://github.com/user/repo/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://github.com/user/repo/blob/master/README.md?plain=1#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blob/master/README.md?plain=1#L5-L7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md?plain=1#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md?plain=1#L5-L7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_url_space(self):
        parse_result = RepositoryParser('git@github.com:user/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('github.com', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://github.com/user/repo/blob/master/path%20with/spaces.txt',
                         parse_result.get_source_url('path with/spaces.txt', 'master'))
        self.assertEqual('https://github.com/user/repo/blob/master/path%20with/spaces.txt?plain=1#L5',
                         parse_result.get_source_url('path with/spaces.txt', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blob/master/path%20with/spaces.txt?plain=1#L5-L7',
                         parse_result.get_source_url('path with/spaces.txt', 'master', 5, 7))
        self.assertEqual('https://github.com/user/repo/blame/master/path%20with/spaces.txt',
                         parse_result.get_blame_url('path with/spaces.txt', 'master'))
        self.assertEqual('https://github.com/user/repo/blame/master/path%20with/spaces.txt?plain=1#L5',
                         parse_result.get_blame_url('path with/spaces.txt', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blame/master/path%20with/spaces.txt?plain=1#L5-L7',
                         parse_result.get_blame_url('path with/spaces.txt', 'master', 5, 7))

    def test_url_hash(self):
        parse_result = RepositoryParser('git@github.com:user/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('github.com', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://github.com/user/repo/blob/master/C%23.txt',
                         parse_result.get_source_url('C#.txt', 'master'))
        self.assertEqual('https://github.com/user/repo/blob/master/C%23.txt?plain=1#L5',
                         parse_result.get_source_url('C#.txt', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blob/master/C%23.txt?plain=1#L5-L7',
                         parse_result.get_source_url('C#.txt', 'master', 5, 7))
        self.assertEqual('https://github.com/user/repo/blame/master/C%23.txt',
                         parse_result.get_blame_url('C#.txt', 'master'))
        self.assertEqual('https://github.com/user/repo/blame/master/C%23.txt?plain=1#L5',
                         parse_result.get_blame_url('C#.txt', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blame/master/C%23.txt?plain=1#L5-L7',
                         parse_result.get_blame_url('C#.txt', 'master', 5, 7))


class RepoParserGitLab(TestCase):

    def test_ssh(self):
        parse_result = RepositoryParser('git@gitlab.com:user/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('gitlab.com', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gitlab.com/user/repo/-/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://gitlab.com/user/repo/-/blob/master/README.md?plain=1#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.com/user/repo/-/blob/master/README.md?plain=1#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://gitlab.com/user/repo/-/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://gitlab.com/user/repo/-/blame/master/README.md?plain=1#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.com/user/repo/-/blame/master/README.md?plain=1#L5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https(self):
        parse_result = RepositoryParser('https://gitlab.com/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('gitlab.com', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gitlab.com/user/repo/-/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://gitlab.com/user/repo/-/blob/master/README.md?plain=1#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.com/user/repo/-/blob/master/README.md?plain=1#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://gitlab.com/user/repo/-/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://gitlab.com/user/repo/-/blame/master/README.md?plain=1#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.com/user/repo/-/blame/master/README.md?plain=1#L5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_ssh_selfhost(self):
        parse_result = RepositoryParser('git@gitlab.selfhost.io:user/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('gitlab.selfhost.io', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blob/master/README.md?plain=1#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blob/master/README.md?plain=1#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blame/master/README.md?plain=1#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blame/master/README.md?plain=1#L5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https_selfhost(self):
        parse_result = RepositoryParser('https://gitlab.selfhost.io/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('gitlab.selfhost.io', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blob/master/README.md?plain=1#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blob/master/README.md?plain=1#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blame/master/README.md?plain=1#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blame/master/README.md?plain=1#L5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_ssh_groups(self):
        parse_result = RepositoryParser('git@gitlab.com:group1/group2/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('gitlab.com', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('group1/group2', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gitlab.com/group1/group2/repo/-/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://gitlab.com/group1/group2/repo/-/blob/master/README.md?plain=1#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.com/group1/group2/repo/-/blob/master/README.md?plain=1#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://gitlab.com/group1/group2/repo/-/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://gitlab.com/group1/group2/repo/-/blame/master/README.md?plain=1#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.com/group1/group2/repo/-/blame/master/README.md?plain=1#L5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))


class RepoParserGitWeb(TestCase):

    def test_ssh(self):
        parse_result = RepositoryParser('git@gitweb.example.com:user/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('gitweb.example.com', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gitweb.example.com/repo/blob/master:/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://gitweb.example.com/repo/blob/master:/README.md#l5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://gitweb.example.com/repo/blob/master:/README.md#l5',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://gitweb.example.com/repo/blame/master:/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://gitweb.example.com/repo/blame/master:/README.md#l5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://gitweb.example.com/repo/blame/master:/README.md#l5',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https(self):
        parse_result = RepositoryParser('https://gitweb.example.com/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('gitweb.example.com', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gitweb.example.com/repo/blob/master:/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://gitweb.example.com/repo/blob/master:/README.md#l5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://gitweb.example.com/repo/blob/master:/README.md#l5',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://gitweb.example.com/repo/blame/master:/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://gitweb.example.com/repo/blame/master:/README.md#l5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://gitweb.example.com/repo/blame/master:/README.md#l5',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))


class RepoParserPagure(TestCase):

    def test_ssh(self):
        parse_result = RepositoryParser('git@pagure.io:user/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('pagure.io', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://pagure.io/user/repo/blob/master/f/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://pagure.io/user/repo/blob/master/f/README.md#_5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://pagure.io/user/repo/blob/master/f/README.md#_5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://pagure.io/user/repo/blame/README.md?identifier=master',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://pagure.io/user/repo/blame/README.md?identifier=master#_5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://pagure.io/user/repo/blame/README.md?identifier=master#_5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https(self):
        parse_result = RepositoryParser('https://pagure.io/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('pagure.io', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://pagure.io/user/repo/blob/master/f/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://pagure.io/user/repo/blob/master/f/README.md#_5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://pagure.io/user/repo/blob/master/f/README.md#_5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://pagure.io/user/repo/blame/README.md?identifier=master',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://pagure.io/user/repo/blame/README.md?identifier=master#_5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://pagure.io/user/repo/blame/README.md?identifier=master#_5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))


class RepoParserPhorge(TestCase):

    def test_ssh(self):
        parse_result = RepositoryParser('ssh://git@we.phorge.it/user/repo-id/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('we.phorge.it', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo-id', parse_result.repo_name)
        self.assertEqual('https://we.phorge.it/user/repo-id/browse/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://we.phorge.it/user/repo-id/browse/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://we.phorge.it/user/repo-id/browse/master/README.md#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://we.phorge.it/user/repo-id/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://we.phorge.it/user/repo-id/blame/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://we.phorge.it/user/repo-id/blame/master/README.md#L5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https(self):
        parse_result = RepositoryParser('https://we.phorge.it/user/repo-id/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('we.phorge.it', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo-id', parse_result.repo_name)
        self.assertEqual('https://we.phorge.it/user/repo-id/browse/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://we.phorge.it/user/repo-id/browse/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://we.phorge.it/user/repo-id/browse/master/README.md#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://we.phorge.it/user/repo-id/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://we.phorge.it/user/repo-id/blame/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://we.phorge.it/user/repo-id/blame/master/README.md#L5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))


class RepoParserRadicle(TestCase):

    def test_https(self):
        parse_result = RepositoryParser('https://seed.radicle.garden/z37oHWbEomJXUAqxd9hoQHWkg2pC8.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('seed.radicle.garden', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual(None, parse_result.owner)
        self.assertEqual('z37oHWbEomJXUAqxd9hoQHWkg2pC8', parse_result.repo_name)
        self.assertEqual('https://app.radicle.xyz/nodes/seed.radicle.garden/rad:z37oHWbEomJXUAqxd9hoQHWkg2pC8/tree/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://app.radicle.xyz/nodes/seed.radicle.garden/rad:z37oHWbEomJXUAqxd9hoQHWkg2pC8/tree/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://app.radicle.xyz/nodes/seed.radicle.garden/rad:z37oHWbEomJXUAqxd9hoQHWkg2pC8/tree/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5, 7))


class RepoParserRhodeCode(TestCase):

    def test_ssh(self):
        parse_result = RepositoryParser('ssh://rhodecode@code.rhodecode.com:3022/repo')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('code.rhodecode.com', parse_result.domain)
        self.assertEqual('rhodecode', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual(None, parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://code.rhodecode.com/repo/files/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://code.rhodecode.com/repo/files/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://code.rhodecode.com/repo/files/master/README.md#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://code.rhodecode.com/repo/annotate/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://code.rhodecode.com/repo/annotate/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://code.rhodecode.com/repo/annotate/master/README.md#L5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https(self):
        parse_result = RepositoryParser('https://code.rhodecode.com/repo')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('code.rhodecode.com', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual(None, parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://code.rhodecode.com/repo/files/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://code.rhodecode.com/repo/files/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://code.rhodecode.com/repo/files/master/README.md#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://code.rhodecode.com/repo/annotate/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://code.rhodecode.com/repo/annotate/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://code.rhodecode.com/repo/annotate/master/README.md#L5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))


class RepoParserSourceForge(TestCase):

    def test_git(self):
        parse_result = RepositoryParser('git://git.code.sf.net/p/user/repo')
        self.assertEqual('git', parse_result.scheme)
        self.assertEqual('git.code.sf.net', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://sourceforge.net/p/user/repo/ci/master/tree/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://sourceforge.net/p/user/repo/ci/master/tree/README.md',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://sourceforge.net/p/user/repo/ci/master/tree/README.md',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://sourceforge.net/p/user/repo/ci/master/tree/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://sourceforge.net/p/user/repo/ci/master/tree/README.md',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://sourceforge.net/p/user/repo/ci/master/tree/README.md',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https(self):
        parse_result = RepositoryParser('https://git.code.sf.net/p/user/repo')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('git.code.sf.net', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://sourceforge.net/p/user/repo/ci/master/tree/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://sourceforge.net/p/user/repo/ci/master/tree/README.md',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://sourceforge.net/p/user/repo/ci/master/tree/README.md',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://sourceforge.net/p/user/repo/ci/master/tree/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://sourceforge.net/p/user/repo/ci/master/tree/README.md',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://sourceforge.net/p/user/repo/ci/master/tree/README.md',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))


class RepoParserSourcehut(TestCase):

    def test_ssh(self):
        parse_result = RepositoryParser('git@git.sr.ht:~user/repo')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('git.sr.ht', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('~user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://git.sr.ht/~user/repo/tree/master/item/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://git.sr.ht/~user/repo/tree/master/item/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://git.sr.ht/~user/repo/tree/master/item/README.md#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://git.sr.ht/~user/repo/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://git.sr.ht/~user/repo/blame/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://git.sr.ht/~user/repo/blame/master/README.md#L5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_https(self):
        parse_result = RepositoryParser('https://git.sr.ht/~user/repo')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('git.sr.ht', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('~user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://git.sr.ht/~user/repo/tree/master/item/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://git.sr.ht/~user/repo/tree/master/item/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://git.sr.ht/~user/repo/tree/master/item/README.md#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://git.sr.ht/~user/repo/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://git.sr.ht/~user/repo/blame/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://git.sr.ht/~user/repo/blame/master/README.md#L5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))


class RepoParserTangled(TestCase):

    def test_ssh(self):
        parse_result = RepositoryParser('git@tangled.org:tangled.org/core')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('tangled.org', parse_result.domain)
        self.assertEqual('git', parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('tangled.org', parse_result.owner)
        self.assertEqual('core', parse_result.repo_name)
        self.assertEqual('https://tangled.org/tangled.org/core/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://tangled.org/tangled.org/core/blob/master/README.md?code=true#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://tangled.org/tangled.org/core/blob/master/README.md?code=true#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))

    def test_https(self):
        parse_result = RepositoryParser('https://tangled.org/tangled.org/core')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('tangled.org', parse_result.domain)
        self.assertEqual(None, parse_result.logon_user)
        self.assertEqual(None, parse_result.logon_password)
        self.assertEqual('tangled.org', parse_result.owner)
        self.assertEqual('core', parse_result.repo_name)
        self.assertEqual('https://tangled.org/tangled.org/core/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://tangled.org/tangled.org/core/blob/master/README.md?code=true#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://tangled.org/tangled.org/core/blob/master/README.md?code=true#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
