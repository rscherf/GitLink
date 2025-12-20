import re
from urllib.parse import quote, urlparse


class RepositoryParser(object):

    REPO_HOSTS = {
        'github': {
            'url': 'https://github.com/{owner}/{repo}/blob/{revision}/{file}',
            'blame_url': 'https://github.com/{owner}/{repo}/blame/{revision}/{file}',
            'line_param': '?plain=1#L',
            'line_param_sep': '-L',
        },
        'bitbucket': {
            'url': 'https://bitbucket.org/{owner}/{repo}/src/{revision}/{file}',
            'blame_url': 'https://bitbucket.org/{owner}/{repo}/annotate/{revision}/{file}',
            'line_param': '#cl-',
            'line_param_sep': ':',
        },
        'codebasehq': {
            'url': 'https://{owner}.{domain}/projects/{project}/repositories/{repo}/blob/{revision}/{file}',
            'blame_url': 'https://{owner}.{domain}/projects/{project}/repositories/{repo}/blame/{revision}/{file}',
            'line_param': '#L',
            'line_param_sep': ':',
        },
        'gitlab': {
            'url': 'https://{domain}/{owner}/{repo}/-/blob/{revision}/{file}',
            'blame_url': 'https://{domain}/{owner}/{repo}/-/blame/{revision}/{file}',
            'line_param': '?plain=1#L',
            'line_param_sep': '-',
        },
        'forgejo': {
            'url': 'https://{domain}/{owner}/{repo}/src/{revision}/{file}',
            'blame_url': 'https://{domain}/{owner}/{repo}/blame/{revision}/{file}',
            'line_param': '?display=source#L',
            'line_param_sep': '-L',
        },
        'sr.ht': {
            'url': 'https://{domain}/{owner}/{repo}/tree/{revision}/item/{file}',
            'blame_url': 'https://{domain}/{owner}/{repo}/blame/{revision}/{file}',
            'line_param': '#L',
            'line_param_sep': '-',
        },
        'gitee': {
            'url': 'https://{domain}/{owner}/{repo}/blob/{revision}/{file}',
            'blame_url': 'https://{domain}/{owner}/{repo}/blame/{revision}/{file}',
            'line_param': '#L',
            'line_param_sep': '-',
        },
        'cgit': {
            'url': 'https://{domain}/{owner}/{repo}/tree/{file}?id={revision}',
            'blame_url': 'https://{domain}/{owner}/{repo}/blame/{file}?id={revision}',
            'line_param': '#n',
            # 'line_param_sep': '-',
        },
    }
    REPO_ALIASES = {
        'gitea': 'forgejo',
        'codeberg': 'forgejo',
    }

    def __init__(self, git_url, ref_type='abbrev'):
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
            self.ssh_user, self.domain = parsed_url.netloc.split('@')
        except:
            self.ssh_user = None
            self.domain = parsed_url.netloc

        path = re.sub(r'\.git$', '', parsed_url.path)
        split_path = path.split('/')
        self.owner = split_path[1]
        self.repo_name = split_path[-1]
        self.project = None

        self.host_type, self.host_formats = self._get_repo_host()

        # Extra rules for specific hosts
        if self.host_type == 'codebasehq':
            self.project = split_path[2]
            if 'http' in self.scheme:
                self.owner = self.domain.split('.')[0]
                self.project = split_path[1]
            self.domain = re.sub(r'^{}\.'.format(self.owner), '', self.domain)

        elif self.host_type == 'gitlab' and len(split_path) > 3:
            self.owner = '/'.join(split_path[1:-1])

    def _get_repo_host(self):
        # Select the right hosting configuration
        success = False
        for repo_host_type, repo_host_fmts in self.REPO_HOSTS.items():
            if repo_host_type in self.domain:
                # We found a match, so keep these variable assignments
                success = True
                break
        if not success:
            for repo_alias, alias_target in self.REPO_ALIASES.items():
                if repo_alias in self.domain:
                    # We found a match, so keep these variable assignments
                    repo_host_type = alias_target
                    repo_host_fmts = self.REPO_HOSTS[alias_target]
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

        url = self.host_formats[fmt_id].format(
            domain=self.domain,
            owner=self.owner,
            project=self.project,
            repo=self.repo_name,
            revision=rev,
            file=quote(file))

        if line_start:
            url += self.host_formats['line_param'] + str(line_start)
            if line_end and line_end != line_start:
                url += self.host_formats['line_param_sep'] + str(line_end)

        return url

    def get_source_url(self, file, revision, line_start=0, line_end=0):
        return self._get_formatted_url('url', file, revision, line_start, line_end)

    def get_blame_url(self, file, revision, line_start=0, line_end=0):
        return self._get_formatted_url('blame_url', file, revision, line_start, line_end)
