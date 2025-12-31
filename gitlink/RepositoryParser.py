import re
import sublime

from urllib.parse import quote, urlparse


class RepositoryParser(object):

    def _load_settings(self):
        settings = sublime.load_settings('GitLink.sublime-settings')
        self.REPO_HOSTS = dict(settings.get('user_repo_hosts'))
        self.REPO_HOSTS.update(settings.get('default_repo_hosts'))
        self.REPO_LOOKUP = dict(settings.get('user_repo_lookup'))
        self.REPO_LOOKUP.update(settings.get('default_repo_lookup'))

    def __init__(self, git_url, ref_type='abbrev'):
        self._load_settings()

        self.git_url = git_url
        self.ref_type = ref_type

        if re.match(r'^git@', git_url):
            git_url = 'ssh://' + git_url
        if 'ssh://' in git_url:
            git_url = re.sub(r'\b:(?=[\w~])', '/', git_url, count=1)
        parsed_url = urlparse(git_url)
        self._pr = parsed_url

        self.scheme = parsed_url.scheme
        try:
            self.logon_user, self.domain = parsed_url.netloc.split('@')
        except:
            self.logon_user = None
            self.domain = parsed_url.netloc

        path = re.sub(r'\.git$', '', parsed_url.path)
        split_path = path.split('/')
        self.owner = split_path[1]
        self.repo_name = split_path[-1]
        self.project = None

        self.host_type, self.host_formats = self._get_repo_host()

        # Extra rules for specific hosts
        if self.host_type == 'codebase':
            self.project = split_path[2]
            if 'http' in self.scheme:
                self.owner = self.domain.split('.')[0]
                self.project = split_path[1]
            self.domain = re.sub(r'^{}\.'.format(self.owner), '', self.domain)

        elif self.host_type == 'gitlab' and len(split_path) > 3:
            self.owner = '/'.join(split_path[1:-1])

        elif self.host_type == 'sourceforge' and self.owner == 'p':
            self.owner = split_path[2]

        elif self.host_type == 'phabricator':
            self.repo_name = split_path[2]

    def _get_repo_host(self):
        # Select the right hosting configuration
        success = False
        for domain_regex, repo_host in self.REPO_LOOKUP.items():
            if re.search(domain_regex, self.domain):
                # We found a match, so keep these variable assignments
                repo_host_type = repo_host
                repo_host_fmts = self.REPO_HOSTS[repo_host]
                success = True
                break
        if not success:
            raise NotImplementedError('"{}" not in known Git hosts'.format(self.domain))
        return repo_host_type, repo_host_fmts

    def _get_formatted_url(self, fmt_id, file, revision, line_start=0, line_end=0):
        rev = revision
        if self.host_type == 'forgejo':
            if self.ref_type == 'abbrev':
                rev = 'branch/' + revision
            elif self.ref_type == 'commithash':
                rev = 'commit/' + revision
            else:
                raise NotImplementedError('Unknown ref type: ' + self.ref_type)

        url = self.host_formats['urls'][fmt_id].format(
            domain=self.domain,
            owner=self.owner,
            project=self.project,
            repo=self.repo_name,
            revision=rev,
            file=quote(file))

        if line_start and 'line_params' in self.host_formats:
            url += self.host_formats['line_params']['start'] + str(line_start)
            if line_end and line_end != line_start and 'separator' in self.host_formats['line_params']:
                url += self.host_formats['line_params']['separator'] + str(line_end)

        return url

    def get_source_url(self, file, revision, line_start=0, line_end=0):
        return self._get_formatted_url('source', file, revision, line_start, line_end)

    def get_blame_url(self, file, revision, line_start=0, line_end=0):
        return self._get_formatted_url('blame', file, revision, line_start, line_end)
