import re
import sublime

from enum import Enum
from urllib.parse import quote, urlparse


class RevType(Enum):
    """Setting options for revision type"""

    ABBREV = ('abbrev', ['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    COMMIT_HASH = ('commithash', ['git', 'rev-parse', 'HEAD'])

    def __init__(self, stg_value, git_args):
        self.setting_value = stg_value
        self.git_args = git_args

    @staticmethod
    def from_setting(stg_value):
        for rev_type in RevType:
            if rev_type.setting_value == stg_value:
                return rev_type
        raise KeyError(stg_value + ' not found in RevType')


class RepositoryParser(object):

    def _load_settings(self):
        settings = sublime.load_settings('GitLink.sublime-settings')
        self.REPO_HOSTS = dict(settings.get('user_repo_hosts'))
        self.REPO_HOSTS.update(settings.get('default_repo_hosts'))
        self.REPO_LOOKUP = dict(settings.get('user_repo_lookup'))
        self.REPO_LOOKUP.update(settings.get('default_repo_lookup'))

    def __init__(self, git_url, rev_type=RevType.ABBREV):
        self._load_settings()

        self.git_url = git_url
        self.rev_type = rev_type

        if re.match(r'^git@', git_url):
            git_url = 'ssh://' + git_url
        if 'ssh://' in git_url:
            git_url = re.sub(r'\b:(?=[\w~])', '/', git_url, count=1)
        parsed_url = urlparse(git_url)
        self._pr = parsed_url

        self.scheme = parsed_url.scheme
        self.logon_user = None
        self.logon_password = None
        try:
            self.logon_user, self.domain = parsed_url.netloc.split('@')
            if ':' in self.logon_user:
                self.logon_user, self.logon_password = self.logon_user.split(':')
        except:
            self.domain = parsed_url.netloc

        # Look up the host template
        self.host_type, self.host_template = self._get_repo_host()

        path = re.sub(r'\.git$', '', parsed_url.path)
        split_path = path.split('/')[1:]
        self.owner = split_path[0]
        self.repo_name = split_path[-1]
        self.project = None

        ### Extra rules for specific hosts ####################################

        if self.host_type == 'assembla':
            self.domain = re.sub(r'^git\.', '', self.domain)
            self.owner = None
            self.repo_name = split_path[0]

        elif self.host_type == 'azure':
            self.domain = re.sub(r'ssh\.', '', self.domain)
            if re.match(r'^v\d$', split_path[0]):
                split_path = split_path[1:]
            self.owner = split_path[0]
            self.project = split_path[1]

        elif self.host_type == 'cgit':
            if re.search(r'\bsavannah\b', self.domain):
                self.domain = re.sub(r'^(?:git\.|https\.)?git', 'cgit.git', self.domain)
                if split_path[0] == 'srv':
                    split_path = split_path[1:]
                elif len(split_path) == 1:
                    split_path.insert(0, '')
                split_path[0] = 'cgit'

            elif re.search(r'\btuxfamily\b', self.domain):
                if split_path[0] == 'gitroot':
                    split_path = split_path[1:]

            self.owner = None
            self.project = '/'.join(split_path[:-1])

        elif self.host_type == 'codebase':
            self.project = split_path[1]
            if 'http' in self.scheme:
                self.owner = self.domain.split('.')[0]
                self.project = split_path[0]
            self.domain = re.sub(r'^{}\.'.format(self.owner), '', self.domain)

        elif self.host_type == 'gitlab':
            self.owner = '/'.join(split_path[:-1])

        elif self.host_type == 'phabricator':
            self.repo_name = split_path[1]

        elif self.host_type == 'radicle':
            self.owner = None

        elif self.host_type == 'rhodecode':
            if self.scheme == 'ssh':
                split_path = split_path[1:]
            self.owner = None
            self.repo_name = split_path[0]

        elif self.host_type == 'sourceforge' and self.owner == 'p':
            self.owner = split_path[1]

        ### End extra host rules ##############################################

    def _get_repo_host(self):
        # Select the right hosting configuration
        pattern = '|'.join('({})'.format(patt) for patt in self.REPO_LOOKUP.keys())
        match = re.search(pattern, self.domain)
        if not match:
            raise NotImplementedError('"{}" not in known Git hosts'.format(self.domain))
        host_type = next(
            host_type for host_type, group
            in zip(self.REPO_LOOKUP.values(), match.groups())
            if group is not None
        )
        return host_type, self.REPO_HOSTS[host_type]

    def _get_formatted_url(self, fmt_id, file, revision, line_start=0, line_end=0):
        rev = revision

        ### Extra rules for specific hosts ####################################

        if self.host_type == 'azure':
            if self.rev_type == RevType.ABBREV:
                # GB for Git Branch?
                rev = 'GB' + revision

        elif self.host_type == 'forgejo':
            if self.rev_type == RevType.ABBREV:
                rev = 'branch/' + revision
            elif self.rev_type == RevType.COMMIT_HASH:
                rev = 'commit/' + revision

        ### End extra host rules ##############################################

        url = self.host_template['urls'][fmt_id].format(
            domain=self.domain,
            owner=self.owner,
            project=self.project,
            repo=self.repo_name,
            revision=rev,
            file=quote(file))

        if line_start and 'line_params' in self.host_template:
            url += self.host_template['line_params']['start'] + str(line_start)
            if line_end and line_end != line_start and 'separator' in self.host_template['line_params']:
                url += self.host_template['line_params']['separator'] + str(line_end)

        return url

    def get_source_url(self, file, revision, line_start=0, line_end=0):
        return self._get_formatted_url('source', file, revision, line_start, line_end)

    def get_blame_url(self, file, revision, line_start=0, line_end=0):
        return self._get_formatted_url('blame', file, revision, line_start, line_end)
