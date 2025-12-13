from unittest import TestCase
from ..repoparse.RepositoryParser import RepositoryParser


class RepositoryParserTestCase(TestCase):

    def test_github_ssh(self):
        parse_result = RepositoryParser('git@github.com:user/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('github.com', parse_result.domain)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://github.com/user/repo/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://github.com/user/repo/blob/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blob/master/README.md#L5-L7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md#L5-L7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_github_ssh_with_scheme(self):
        parse_result = RepositoryParser('ssh://git@github.com:user/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('github.com', parse_result.domain)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://github.com/user/repo/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://github.com/user/repo/blob/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blob/master/README.md#L5-L7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md#L5-L7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_github_https(self):
        parse_result = RepositoryParser('https://github.com/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('github.com', parse_result.domain)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://github.com/user/repo/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://github.com/user/repo/blob/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blob/master/README.md#L5-L7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://github.com/user/repo/blame/master/README.md#L5-L7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_bitbucket_ssh(self):
        parse_result = RepositoryParser('git@bitbucket.org:user/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('bitbucket.org', parse_result.domain)
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

    def test_bitbucket_https(self):
        parse_result = RepositoryParser('https://user@bitbucket.org/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('bitbucket.org', parse_result.domain)
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

    def test_bitbucket_https_no_user(self):
        parse_result = RepositoryParser('https://bitbucket.org/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('bitbucket.org', parse_result.domain)
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

    def test_gitlab_ssh(self):
        parse_result = RepositoryParser('git@gitlab.com:user/repo.git')
        self.assertEqual('gitlab.com', parse_result.domain)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gitlab.com/user/repo/-/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://gitlab.com/user/repo/-/blob/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.com/user/repo/-/blob/master/README.md#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://gitlab.com/user/repo/-/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://gitlab.com/user/repo/-/blame/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.com/user/repo/-/blame/master/README.md#L5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_gitlab_https(self):
        parse_result = RepositoryParser('https://gitlab.com/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('gitlab.com', parse_result.domain)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gitlab.com/user/repo/-/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://gitlab.com/user/repo/-/blob/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.com/user/repo/-/blob/master/README.md#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://gitlab.com/user/repo/-/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://gitlab.com/user/repo/-/blame/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.com/user/repo/-/blame/master/README.md#L5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_gitlab_selfhost_ssh(self):
        parse_result = RepositoryParser('git@gitlab.selfhost.io:user/repo.git')
        self.assertEqual('gitlab.selfhost.io', parse_result.domain)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blob/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blob/master/README.md#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blame/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blame/master/README.md#L5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_gitlab_selfhost_https(self):
        parse_result = RepositoryParser('https://gitlab.selfhost.io/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('gitlab.selfhost.io', parse_result.domain)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blob/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blob/master/README.md#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blame/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.selfhost.io/user/repo/-/blame/master/README.md#L5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_gitlab_groups_ssh(self):
        parse_result = RepositoryParser('git@gitlab.com:group1/group2/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('gitlab.com', parse_result.domain)
        self.assertEqual('group1/group2', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://gitlab.com/group1/group2/repo/-/blob/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://gitlab.com/group1/group2/repo/-/blob/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.com/group1/group2/repo/-/blob/master/README.md#L5-7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://gitlab.com/group1/group2/repo/-/blame/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://gitlab.com/group1/group2/repo/-/blame/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://gitlab.com/group1/group2/repo/-/blame/master/README.md#L5-7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_codebasehq_ssh(self):
        parse_result = RepositoryParser('git@codebasehq.com:user/project/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('codebasehq.com', parse_result.domain)
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

    def test_codebasehq_https(self):
        parse_result = RepositoryParser('https://user.codebasehq.com/project/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('codebasehq.com', parse_result.domain)
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

    def test_codeberg_ssh_branch(self):
        parse_result = RepositoryParser('git@codeberg.org:user/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('codeberg.org', parse_result.domain)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://codeberg.org/user/repo/src/branch/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://codeberg.org/user/repo/src/branch/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://codeberg.org/user/repo/src/branch/master/README.md#L5-L7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://codeberg.org/user/repo/blame/branch/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://codeberg.org/user/repo/blame/branch/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://codeberg.org/user/repo/blame/branch/master/README.md#L5-L7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_codeberg_https_branch(self):
        parse_result = RepositoryParser('https://codeberg.org/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('codeberg.org', parse_result.domain)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://codeberg.org/user/repo/src/branch/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://codeberg.org/user/repo/src/branch/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://codeberg.org/user/repo/src/branch/master/README.md#L5-L7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://codeberg.org/user/repo/blame/branch/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://codeberg.org/user/repo/blame/branch/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://codeberg.org/user/repo/blame/branch/master/README.md#L5-L7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_codeberg_ssh_sha(self):
        parse_result = RepositoryParser('git@codeberg.org:user/repo.git', 'commithash')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('codeberg.org', parse_result.domain)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://codeberg.org/user/repo/src/commit/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://codeberg.org/user/repo/src/commit/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://codeberg.org/user/repo/src/commit/master/README.md#L5-L7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://codeberg.org/user/repo/blame/commit/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://codeberg.org/user/repo/blame/commit/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://codeberg.org/user/repo/blame/commit/master/README.md#L5-L7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))

    def test_codeberg_https_sha(self):
        parse_result = RepositoryParser('https://codeberg.org/user/repo.git', 'commithash')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('codeberg.org', parse_result.domain)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('https://codeberg.org/user/repo/src/commit/master/README.md',
                         parse_result.get_source_url('README.md', 'master'))
        self.assertEqual('https://codeberg.org/user/repo/src/commit/master/README.md#L5',
                         parse_result.get_source_url('README.md', 'master', 5))
        self.assertEqual('https://codeberg.org/user/repo/src/commit/master/README.md#L5-L7',
                         parse_result.get_source_url('README.md', 'master', 5, 7))
        self.assertEqual('https://codeberg.org/user/repo/blame/commit/master/README.md',
                         parse_result.get_blame_url('README.md', 'master'))
        self.assertEqual('https://codeberg.org/user/repo/blame/commit/master/README.md#L5',
                         parse_result.get_blame_url('README.md', 'master', 5))
        self.assertEqual('https://codeberg.org/user/repo/blame/commit/master/README.md#L5-L7',
                         parse_result.get_blame_url('README.md', 'master', 5, 7))
