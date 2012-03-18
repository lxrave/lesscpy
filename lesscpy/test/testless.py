"""
    lesscpy tests.
"""
import unittest
import os
import glob
import bootstrap

from lesscpy.lessc import parser
from lesscpy.lessc import formatter

class TestCase(unittest.TestCase):
    pass

def create_test (args):
    def do_test_expected(self):
        lessf, cssf, minf = args
        if os.path.exists(cssf):
            p = parser.LessParser()
            p.parse(filename=lessf)
            f = formatter.Formatter()
            pout = f.format(p).split('\n')
            i = 0
            with open(cssf) as cssf:
                for line in cssf.readlines():
                    line = line.rstrip()
                    if not line: continue
                    self.assertEqual(line, pout[i], '%s: Line %d' % (cssf, i+1))
                    i += 1
            if len(pout) > i and i:
                self.fail("%s: result has more lines (%d < %d)" % (cssf, i, len(pout)))
        else:
            self.fail("%s not found..." % cssf)
        if os.path.exists(minf):
            p = parser.LessParser()
            p.parse(filename=lessf)
            f = formatter.Formatter()
            mout = f.format(p, True).split('\n')
            i = 0
            with open(minf) as cssf:
                for line in cssf.readlines():
                    self.assertEqual(line.rstrip(), mout[i], '%s: Line %d' % (minf, i+1))
                    i += 1
            if len(mout) > i and i:
                self.fail("%s: result has more lines (%d < %d)" % (minf, i, len(mout)))
        else:
            self.fail("%s not found..." % minf)
    return do_test_expected

LESS = glob.glob( os.path.join('less/', '*.less'))
for less in LESS:
    lessf = less.split('.')[0].split('/')[-1]
    css = 'css/' + lessf + '.css'
    mincss = 'css/' + lessf + '.min.css'
    test_method = create_test((less, css, mincss))
    test_method.__name__ = 'test_%s' % less.replace('./-', '_')
    setattr(TestCase, test_method.__name__, test_method)

if __name__=="__main__":
    unittest.main()
