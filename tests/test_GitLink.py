import sublime
import subprocess

from os.path import abspath, dirname, join as pjoin
from unittesting import DeferrableViewTestCase


class GitLinkTestCase(DeferrableViewTestCase):

    @classmethod
    def setUpClass(cls):
        # Prep clipboard to return later
        cls.orig_clipboard = sublime.get_clipboard()

        # Set up the test repo
        my_path = abspath(dirname(__file__))
        clone_path = pjoin(my_path, 'Switcher')
        print(clone_path)
        exitcode, _ = subprocess.getstatusoutput(
            'cd ' + my_path + ' && '
            'git clone https://github.com/rscherf/Switcher.git Switcher')
        print(_)
        cls.repo_path = clone_path # pjoin(clone_path, 'Switcher')
        cls.readme_path =  pjoin(cls.repo_path, 'README.md')

    @classmethod
    def tearDownClass(cls):
        # Restore the clipboard
        sublime.set_clipboard(cls.orig_clipboard)

        # Delete the test repo
        subprocess.getoutput('rm -r ' + cls.repo_path)

    def setUp(self):
        self.view = sublime.active_window().open_file(self.readme_path)
        yield lambda: not self.view.is_loading()

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def test_repo_file_view(self):
        self.assertTrue(self.view.is_valid())
        self.assertTrue(self.view.file_name().replace('\\', '/').endswith('Switcher/README.md'))
        self.assertEqual('Switcher', self.view.substr(self.view.line(0)))

    def test_clipboard_exists(self):
        sublime.set_clipboard('')
        self.assertFalse(sublime.get_clipboard())
        sublime.set_clipboard('test string')
        self.assertEqual('test string', sublime.get_clipboard())

    def test_copy_url(self):
        sublime.set_clipboard('')
        self.view.run_command('gitlink', {'web': False, 'line': False})
        yield {
            'condition': lambda: sublime.get_clipboard() != '',
            'period': 200,
            'timeout': 20 * 1000,
            'timeout_message': 'Clipboard is still blank',
        }
        self.assertEqual('https://github.com/rscherf/Switcher/blob/master/README.md', sublime.get_clipboard())

    def test_copy_blame(self):
        sublime.set_clipboard('')
        self.view.run_command('gitlink', {'web': False, 'line': False, 'blame': True})
        yield lambda: sublime.get_clipboard() != ""
        self.assertEqual('https://github.com/rscherf/Switcher/blame/master/README.md', sublime.get_clipboard())

    def test_copy_url_line(self):
        sublime.set_clipboard('')
        self.view.run_command('gitlink', {'web': False, 'line': True})
        yield lambda: sublime.get_clipboard() != ""
        self.assertEqual('https://github.com/rscherf/Switcher/blob/master/README.md?plain=1#L1', sublime.get_clipboard())

    def test_copy_blame_line(self):
        sublime.set_clipboard('')
        self.view.run_command('gitlink', {'web': False, 'line': True, 'blame': True})
        yield lambda: sublime.get_clipboard() != ""
        self.assertEqual('https://github.com/rscherf/Switcher/blame/master/README.md?plain=1#L1', sublime.get_clipboard())
