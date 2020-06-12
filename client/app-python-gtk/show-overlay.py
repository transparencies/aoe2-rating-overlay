# This file contains code from svgoverlay,
# Taken from https://gist.github.com/seigler/28dd06334b55a93692855a8dd62c1b57
# Copyright 2017-2020 Joshua Seigler.
# It's licensed under the terms of the MIT license.
# Modifications Copyright 2020-2020 the aoe-assoc authors.
# See COPYING.md for further legal info.

# svgoverlay
# Display an SVG from disk or URL in a fullscreen, transparent, click-through window, with settable opacity.
# When used on Arch Linux, requires AUR package python-gobject-patched for click-through functionality
#
# Example usage:
# svgoverlay --opacity 0.8 --monitor 0 filename.svg

import sys

import argparse
import cairo
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import Gio
from gi.repository import GLib
from urllib.request import urlopen

# def get_image_data(image_path):
#     if image_path.startswith('http://') or image_path.startswith('https://'):
#         # If the image path is a URL, fetch it
#         return bytearray(urlopen(image_path).read())
#     else:
#         # Else, load it from distk
#         with open(image_path, 'rb') as f:
#             return bytearray(f.read())
#

class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        outerbox = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.add(outerbox)
        outerbox.show()

        builder = Gtk.Builder()
        builder.add_from_file("./ui/main.glade")
        menu = builder.get_object("app-menu")

        button = Gtk.MenuButton.new()
        popover = Gtk.Popover.new_from_model(button, menu)
        button.set_popover(popover)

        outerbox.pack_start(button, False, True, 0)
        button.show()
        self.set_border_width(50)


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.aoe2assoc.overlay-desktop", **kwargs)
        self.window = None

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
            self.window = AppWindow(application=self, title="Main Window")

        self.window.present()

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()


# class SvgOverlay(Gtk.Window):
#     # TODO: Make window resizable and svg scale in it
#     # TODO: Make window draggable with mouse and lock in place with an option
#     # TODO: Open options menu with a long click on the overlay
#
#     def __init__(self, image_path, fixed, reload, monitor, opacity):
#         Gtk.Window.__init__(self, title="svgoverlay")
#         self.opacity = opacity
#
#         self.screen = self.get_screen()
#         self.visual = self.screen.get_rgba_visual()
#         if self.visual is not None and self.screen.is_composited():
#             self.set_visual(self.visual)
#
#         # Move to specified monitor
#         # TODO: Refactor, this is deprecated
#         geometry = self.screen.get_monitor_geometry(monitor)
#         self.move(geometry.x, geometry.y)
#
#         # Set full screen window properties
#         self.set_decorated(False)
#         self.set_modal(True)
#         self.set_keep_above(True)
#         self.set_accept_focus(False)
#         self.set_app_paintable(True)
#         self.set_skip_taskbar_hint(True)
#         self.set_skip_pager_hint(True)
#         self.fullscreen()
#
#         # Get image width and height
#         self.image_size = (geometry.width, geometry.height)
#
#         if fixed:
#             # If in fixed mode, create a fixed GTK container and set image width and height to provided
#             self.fixed_container = Gtk.Fixed()
#             self.image_size = [int(n) for n in fixed.split(',')]
#
#         # Create image
#         self.image_path = image_path
#         self.svg_image = Gtk.Image()
#         self.svg_image.set_opacity(opacity)
#         self.reload_image()
#
#         # Add fixed container or full image
#         if fixed:
#             self.fixed_container.put(self.svg_image, self.image_size[2], self.image_size[3])
#             self.add(self.fixed_container)
#         else:
#             self.add(self.svg_image)
#
#         # Set reload interval if provided
#         if reload:
#             GLib.timeout_add_seconds(reload, self.reload_image)
#
#         self.connect("draw", self.on_draw)
#
#     def reload_image(self):
#         # Reload the image
#         input_stream = Gio.MemoryInputStream.new_from_data(get_image_data(self.image_path), None)
#         pixbuf = Pixbuf.new_from_stream_at_scale(input_stream, self.image_size[0], self.image_size[1], True, None)
#         self.svg_image.set_from_pixbuf(pixbuf)
#         return True
#
#     def on_draw(self, widget, cr):
#         # Handle clickthrough
#         cr.set_source_rgba(0.0, 0.0, 0.0, 0.0)
#         cr.set_operator(cairo.OPERATOR_SOURCE)
#         cr.paint()
#         cr.set_operator(cairo.OPERATOR_OVER)
#         self.input_shape_combine_region(cairo.Region(cairo.RectangleInt(0, 0, 0, 0)))
#

# class SvgOverlayMenuBar(Gtk.MenuBar):
#     def __init__(self=None):
#         Gtk.MenuBar.__init__(self, title="")
# Show MenuBar
# Hide MenuBar


if __name__ == '__main__':
    # import signal
    #
    # signal.signal(signal.SIGINT, signal.SIG_DFL)
    #
    # parser = argparse.ArgumentParser(description='Display a transparent, clickthrough SVG image overlay')
    # parser.add_argument('--opacity', type=float, help='decimal; opacity of image displayed')
    # parser.add_argument('--monitor', type=int, help='monitor to display overlay on')
    # parser.add_argument('--fixed', type=str, help='display image in fixed region instead of scaling; provide as '
    #                                               'width,height,y,x')
    # parser.add_argument('--resizable', type=str, help='make image resizable by dragging the mouse on the windows '
    #                                                   'borders')  # TODO!
    # parser.add_argument('--draggable', type=str,
    #                     help='make image draggable by clicking on it 5s and move the mouse')  # TODO!
    # parser.add_argument('--reload', type=float, help='reload the image every specified seconds')
    # parser.add_argument('image', type=str, help='path or url to SVG to display')
    #
    # args = parser.parse_args()

    # win = SvgOverlay(args.image, args.fixed, args.reload, args.monitor or 0, args.opacity or 1.0)
    # win.connect("destroy", Gtk.main_quit)
    # win.show_all()
    # Gtk.main()

    app = Application()
    app.run(sys.argv)
