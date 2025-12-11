import unittest
from RepositoryParser import RepositoryParser


class RepositoryParserTestCase(unittest.TestCase):

    def test_github_simple(self):
        parse_result = RepositoryParser('git@github.com:user/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('github.com', parse_result.domain)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)

        parse_result = RepositoryParser('https://github.com/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('github.com', parse_result.domain)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)

    def test_gitlab_simple(self):
        parse_result = RepositoryParser('git@gitlab.com:user/repo.git')
        self.assertEqual('gitlab.com', parse_result.domain)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)

        parse_result = RepositoryParser('https://gitlab.com/user/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('gitlab.com', parse_result.domain)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)

    def test_gitlab_groups(self):
        parse_result = RepositoryParser('git@gitlab.selfhost.io:group1/group2/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('gitlab.selfhost.io', parse_result.domain)
        self.assertEqual('group1/group2', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)

    def test_codebasehq(self):
        parse_result = RepositoryParser('git@codebasehq.com:user/project/repo.git')
        self.assertEqual('ssh', parse_result.scheme)
        self.assertEqual('codebasehq.com', parse_result.domain)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('project', parse_result.project)

        parse_result = RepositoryParser('https://user.codebasehq.com/project/repo.git')
        self.assertEqual('https', parse_result.scheme)
        self.assertEqual('user.codebasehq.com', parse_result.domain)
        self.assertEqual('user', parse_result.owner)
        self.assertEqual('repo', parse_result.repo_name)
        self.assertEqual('project', parse_result.project)
