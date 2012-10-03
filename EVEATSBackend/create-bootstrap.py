#!/usr/bin/env python
# vim: fileencoding=utf8
from virtualenv import create_bootstrap_script

EXTRA_TEXT = """
import os

def after_install(options, home_dir):
    cmd = [os.path.join(home_dir, 'bin', 'pip')]
    cmd += 'install -r requirements.txt'.split()
    call_subprocess(cmd)
"""

if __name__ == '__main__':
    print create_bootstrap_script(EXTRA_TEXT)
