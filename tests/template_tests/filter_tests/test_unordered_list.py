import warnings

from django.template.defaultfilters import unordered_list
from django.test import SimpleTestCase
from django.utils.deprecation import RemovedInDjango20Warning
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe

from ..utils import setup


class UnorderedListTests(SimpleTestCase):

    @setup({'unordered_list01': '{{ a|unordered_list }}'})
    def test_unordered_list01(self):
        output = self.engine.render_to_string('unordered_list01', {'a': ['x>', ['<y']]})
        self.assertEqual(output, '\t<li>x&gt;\n\t<ul>\n\t\t<li>&lt;y</li>\n\t</ul>\n\t</li>')

    @setup({'unordered_list02': '{% autoescape off %}{{ a|unordered_list }}{% endautoescape %}'})
    def test_unordered_list02(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', RemovedInDjango20Warning)
            output = self.engine.render_to_string('unordered_list02', {'a': ['x>', ['<y']]})
        self.assertEqual(output, '\t<li>x>\n\t<ul>\n\t\t<li><y</li>\n\t</ul>\n\t</li>')

    @setup({'unordered_list03': '{{ a|unordered_list }}'})
    def test_unordered_list03(self):
        output = self.engine.render_to_string('unordered_list03', {'a': ['x>', [mark_safe('<y')]]})
        self.assertEqual(output, '\t<li>x&gt;\n\t<ul>\n\t\t<li><y</li>\n\t</ul>\n\t</li>')

    @setup({'unordered_list04': '{% autoescape off %}{{ a|unordered_list }}{% endautoescape %}'})
    def test_unordered_list04(self):
        output = self.engine.render_to_string('unordered_list04', {'a': ['x>', [mark_safe('<y')]]})
        self.assertEqual(output, '\t<li>x>\n\t<ul>\n\t\t<li><y</li>\n\t</ul>\n\t</li>')

    @setup({'unordered_list05': '{% autoescape off %}{{ a|unordered_list }}{% endautoescape %}'})
    def test_unordered_list05(self):
        output = self.engine.render_to_string('unordered_list05', {'a': ['x>', ['<y']]})
        self.assertEqual(output, '\t<li>x>\n\t<ul>\n\t\t<li><y</li>\n\t</ul>\n\t</li>')


class DeprecatedUnorderedListSyntaxTests(SimpleTestCase):

    @setup({'unordered_list01': '{{ a|unordered_list }}'})
    def test_unordered_list01(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', RemovedInDjango20Warning)
            output = self.engine.render_to_string('unordered_list01', {'a': ['x>', [['<y', []]]]})
        self.assertEqual(output, '\t<li>x&gt;\n\t<ul>\n\t\t<li>&lt;y</li>\n\t</ul>\n\t</li>')

    @setup({'unordered_list02': '{% autoescape off %}{{ a|unordered_list }}{% endautoescape %}'})
    def test_unordered_list02(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', RemovedInDjango20Warning)
            output = self.engine.render_to_string('unordered_list02', {'a': ['x>', [['<y', []]]]})
        self.assertEqual(output, '\t<li>x>\n\t<ul>\n\t\t<li><y</li>\n\t</ul>\n\t</li>')

    @setup({'unordered_list03': '{{ a|unordered_list }}'})
    def test_unordered_list03(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', RemovedInDjango20Warning)
            output = self.engine.render_to_string('unordered_list03', {'a': ['x>', [[mark_safe('<y'), []]]]})
        self.assertEqual(output, '\t<li>x&gt;\n\t<ul>\n\t\t<li><y</li>\n\t</ul>\n\t</li>')

    @setup({'unordered_list04': '{% autoescape off %}{{ a|unordered_list }}{% endautoescape %}'})
    def test_unordered_list04(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', RemovedInDjango20Warning)
            output = self.engine.render_to_string('unordered_list04', {'a': ['x>', [[mark_safe('<y'), []]]]})
        self.assertEqual(output, '\t<li>x>\n\t<ul>\n\t\t<li><y</li>\n\t</ul>\n\t</li>')

    @setup({'unordered_list05': '{% autoescape off %}{{ a|unordered_list }}{% endautoescape %}'})
    def test_unordered_list05(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', RemovedInDjango20Warning)
            output = self.engine.render_to_string('unordered_list05', {'a': ['x>', [['<y', []]]]})
        self.assertEqual(output, '\t<li>x>\n\t<ul>\n\t\t<li><y</li>\n\t</ul>\n\t</li>')


class FunctionTests(SimpleTestCase):

    def test_list(self):
        self.assertEqual(unordered_list(['item 1', 'item 2']), '\t<li>item 1</li>\n\t<li>item 2</li>')

    def test_nested(self):
        self.assertEqual(
            unordered_list(['item 1', ['item 1.1']]),
            '\t<li>item 1\n\t<ul>\n\t\t<li>item 1.1</li>\n\t</ul>\n\t</li>',
        )

    def test_nested2(self):
        self.assertEqual(
            unordered_list(['item 1', ['item 1.1', 'item1.2'], 'item 2']),
            '\t<li>item 1\n\t<ul>\n\t\t<li>item 1.1</li>\n\t\t<li>item1.2'
            '</li>\n\t</ul>\n\t</li>\n\t<li>item 2</li>',
        )

    def test_nested_multiple(self):
        self.assertEqual(
            unordered_list(['item 1', ['item 1.1', ['item 1.1.1', ['item 1.1.1.1']]]]),
            '\t<li>item 1\n\t<ul>\n\t\t<li>item 1.1\n\t\t<ul>\n\t\t\t<li>'
            'item 1.1.1\n\t\t\t<ul>\n\t\t\t\t<li>item 1.1.1.1</li>\n\t\t\t'
            '</ul>\n\t\t\t</li>\n\t\t</ul>\n\t\t</li>\n\t</ul>\n\t</li>',
        )

    def test_nested_multiple2(self):
        self.assertEqual(
            unordered_list(['States', ['Kansas', ['Lawrence', 'Topeka'], 'Illinois']]),
            '\t<li>States\n\t<ul>\n\t\t<li>Kansas\n\t\t<ul>\n\t\t\t<li>'
            'Lawrence</li>\n\t\t\t<li>Topeka</li>\n\t\t</ul>\n\t\t</li>'
            '\n\t\t<li>Illinois</li>\n\t</ul>\n\t</li>',
        )

    def test_ulitem(self):
        @python_2_unicode_compatible
        class ULItem(object):
            def __init__(self, title):
                self.title = title

            def __str__(self):
                return 'ulitem-%s' % str(self.title)

        a = ULItem('a')
        b = ULItem('b')
        self.assertEqual(unordered_list([a, b]), '\t<li>ulitem-a</li>\n\t<li>ulitem-b</li>')

        def item_generator():
            yield a
            yield b

        self.assertEqual(unordered_list(item_generator()), '\t<li>ulitem-a</li>\n\t<li>ulitem-b</li>')

    def test_legacy(self):
        """
        Old format for unordered lists should still work
        """
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', RemovedInDjango20Warning)

            self.assertEqual(unordered_list(['item 1', []]), '\t<li>item 1</li>')

            self.assertEqual(
                unordered_list(['item 1', [['item 1.1', []]]]),
                '\t<li>item 1\n\t<ul>\n\t\t<li>item 1.1</li>\n\t</ul>\n\t</li>',
            )

            self.assertEqual(
                unordered_list(['item 1', [['item 1.1', []],
                ['item 1.2', []]]]), '\t<li>item 1\n\t<ul>\n\t\t<li>item 1.1'
                '</li>\n\t\t<li>item 1.2</li>\n\t</ul>\n\t</li>',
            )

            self.assertEqual(
                unordered_list(['States', [['Kansas', [['Lawrence', []], ['Topeka', []]]], ['Illinois', []]]]),
                '\t<li>States\n\t<ul>\n\t\t<li>Kansas\n\t\t<ul>\n\t\t\t<li>Lawrence</li>'
                '\n\t\t\t<li>Topeka</li>\n\t\t</ul>\n\t\t</li>\n\t\t<li>Illinois</li>\n\t</ul>\n\t</li>',
            )
