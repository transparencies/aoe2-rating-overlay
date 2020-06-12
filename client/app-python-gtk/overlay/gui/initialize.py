# As well as code from PyGObject-Tutorial,
# Taken from https://github.com/sebp/PyGObject-Tutorial/blob/master/examples/application_example.py
# Copyright 2016-2019 Sebastian Pölsterl.
# It's licensed under the terms of the Free Documentation License 1.3 Revision 3cd49b0a.
#
# Modifications Copyright 2020-2020 the aoe-assoc authors.
# See COPYING.md for further legal info.

import cairo
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import Gio
from gi.repository import GLib
from urllib.request import urlopen


class ApplicationWindows(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        outerbox = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.add(outerbox)
        outerbox.show()

        builder = Gtk.Builder()
        builder.add_from_file("overlay/gui/application.glade")

        window = builder.get_object("AppWindow")
