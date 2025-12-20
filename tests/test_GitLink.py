import sublime

from unittesting import DeferrableViewTestCase


class GitLinkTestCase(DeferrableViewTestCase):

    def setUp(self):
        self.view = sublime.active_window().open_file('tests/Switcher/README.md')

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def test_repo_file_view(self):
        self.assertTrue(self.view.is_valid())
        self.assertTrue(self.view.file_name().replace('\\', '/').endswith('Switcher/README.md'))

    def test_copy_url(self):
        sublime.set_clipboard('')
        self.view.run_command('gitlink', {'web': False, 'line': False})
        yield lambda: sublime.get_clipboard() != ""
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
