#!/usr/bin/env python
#
# Run the test suite against all the Python versions we can find.
#

from __future__ import print_function

import sys
import os
from os.path import dirname, abspath, join
import re


TOP = dirname(dirname(abspath(__file__)))
sys.path.insert(0, join(TOP, "tools"))
import which


def _python_ver_from_python(python):
    assert ' ' not in python
    o = os.popen('''%s -c "import sys; print(sys.version)"''' % python)
    ver_str = o.read().strip()
    ver_bits = re.split(r"\.|[^\d]", ver_str, 2)[:2]
    ver = tuple(map(int, ver_bits))
    return ver

def _gen_python_names():
    yield "python"
    # generate version numbers from python 3.5 to 3.20
    for ver in [(3, i) for i in range(5, 20)]:
        yield "python%d.%d" % ver
        if sys.platform == "win32":
            yield "python%d%d" % ver

def _gen_pythons():
    python_from_ver = {}
    for name in _gen_python_names():
        for python in which.whichall(name):
            ver = _python_ver_from_python(python)
            if ver not in python_from_ver:
                python_from_ver[ver] = python
    for ver, python in sorted(python_from_ver.items()):
        yield ver, python

def testall():
    for ver, python in _gen_pythons():
        if ver < (3, 5):
            # Don't support Python < 3.5
            continue
        ver_str = "%s.%s" % ver
        print("-- test with Python %s (%s)" % (ver_str, python))
        assert ' ' not in python
        rv = os.system("MACOSX_DEPLOYMENT_TARGET= %s test.py -- -knownfailure" % python)
        if rv:
            sys.exit(os.WEXITSTATUS(rv))

testall()
