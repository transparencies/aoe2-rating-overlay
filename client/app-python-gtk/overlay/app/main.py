# As well as code from PyGObject-Tutorial,
# Taken from https://github.com/sebp/PyGObject-Tutorial/blob/master/examples/application_example.py
# Copyright 2016-2019 Sebastian Pölsterl.
# It's licensed under the terms of the Free Documentation License 1.3 Revision 3cd49b0a.
#
# Modifications Copyright 2020-2020 the aoe-assoc authors.
# See COPYING.md for further legal info.

import cairo
import gi

from overlay.gui.initialize import ApplicationWindows

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import Gio
from gi.repository import GLib
from urllib.request import urlopen


def get_image_data(image_path):
    if image_path.startswith('http://') or image_path.startswith('https://'):
        # If the image path is a URL, fetch it
        return bytearray(urlopen(image_path).read())
    else:
        # Else, load it from distk
        with open(image_path, 'rb') as f:
            return bytearray(f.read())


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.aoe2assoc.overlay-desktop",
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE, **kwargs)
        self.window = None

        self.add_main_option(
            "test",
            ord("t"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            "Command line test",
            None,
        )

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = ApplicationWindows(application=self, title="aoe2overlay")

        self.window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        # convert GVariantDict -> GVariant -> dict
        options = options.end().unpack()

        # TODO: Add to this method
        # parser = argparse.ArgumentParser(description='Display a SVG overlay')
        # parser.add_argument('--opacity', type=float, help='decimal; opacity of image displayed')
        # parser.add_argument('--monitor', type=int, help='monitor to display overlay on')
        # parser.add_argument('--fixed', type=str, help='display image in fixed region instead of scaling; provide as '
        #                                               'width,height,y,x')
        # parser.add_argument('--resizable', type=str, help='make image resizable by dragging the mouse on the windows '
        #                                                   'borders')  # TODO!
        # parser.add_argument('--draggable', type=str,
        #                     help='make image draggable by clicking on it 5s and move the mouse')  # TODO!
        # parser.add_argument('--reload', type=float, help='reload the image every specified seconds')
        # parser.add_argument('--image-path', type=str, help='path or url to SVG to display')
        #
        # args = parser.parse_args()

        if "test" in options:
            # This is printed on the main instance
            print("Test argument recieved: %s" % options["test"])

        self.activate()
        return 0

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()

    def on_draw(self, widget, cr):
        # Handle clickthrough
        cr.set_source_rgba(0.0, 0.0, 0.0, 0.0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)
        self.input_shape_combine_region(cairo.Region(cairo.RectangleInt(0, 0, 0, 0)))

    def reload_image(self):
        # Reload the image
        input_stream = Gio.MemoryInputStream.new_from_data(get_image_data(self.image_path), None)
        pixbuf = Pixbuf.new_from_stream_at_scale(input_stream, self.image_size[0], self.image_size[1], True, None)
        self.svg_image.set_from_pixbuf(pixbuf)
        return True
