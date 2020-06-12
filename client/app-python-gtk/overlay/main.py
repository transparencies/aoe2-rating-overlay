# Copyright 2020-2020 the aoe-assoc authors. See COPYING.md for legal info.

"""
The central entry point.

"""
import sys
from overlay.app.main import Application


if __name__ == '__main__':

    app = Application()
    app.run(sys.argv)
