import cgi

from pygments.formatters import HtmlFormatter


class CodeHtmlFormatter(HtmlFormatter):

    def wrap(self, source, outfile):
        return self._wrap_code(self._wrap_div(self._wrap_pre(source)))

    def _wrap_code(self, source):
        yield 0, '<ol class="highlight">'
        i = 1
        for i, t in source:
            t = t.rstrip()
            if t == "" or t.isspace():
                t = "&nbsp;"
            if i == 1:
                # it's a line of formatted code
                t = '<li id="li_' + str(i) + '">' + t + "</li>"
                i += 1
            yield i, t
        yield 0, '</ol>'
        
    def _wrap_div(self, inner):
        yield 0, ('<div' + (self.cssclass and ' class="%s"' % self.cssclass)
                  + (self.cssstyles and ' style="%s"' % self.cssstyles) + '>')
        for tup in inner:
            yield tup
        yield 0, '</div>\n'

    def _wrap_pre(self, inner):
        yield 0, ('<pre'
                  + (self.prestyles and ' style="%s"' % self.prestyles) + '>')
        for tup in inner:
            yield tup
        yield 0, '</pre>'