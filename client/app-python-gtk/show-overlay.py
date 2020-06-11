#!/usr/bin/env python3
#
# svgoverlay
# Based on Fiverr Job completed by https://www.fiverr.com/nvella
# Fiverr Job FO4F459DA7C8
# Taken from https://gist.github.com/seigler/28dd06334b55a93692855a8dd62c1b57
#
# Display an SVG from disk or URL in a fullscreen, transparent, click-through window, with settable opacity.
# When used on Arch Linux, requires AUR package python-gobject-patched for click-through functionality
#
# Example usage:
# svgoverlay --opacity 0.8 --monitor 0 filename.svg
#

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

class SvgOverlay(Gtk.Window):
    def __init__(self, image_path, fixed, reload, monitor, opacity):
        Gtk.Window.__init__(self, title="svgoverlay")
        self.opacity = opacity

        self.screen = self.get_screen()
        self.visual = self.screen.get_rgba_visual()
        if self.visual != None and self.screen.is_composited():
            self.set_visual(self.visual)

        # Move to specified monitor
        geometry = self.screen.get_monitor_geometry(monitor)
        self.move(geometry.x, geometry.y)

        # Set full screen window properties
        self.set_decorated(False)
        self.set_modal(True)
        self.set_keep_above(True)
        self.set_accept_focus(False)
        self.set_app_paintable(True)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.fullscreen()

        # Get image width and height
        self.image_size = (geometry.width, geometry.height)

        if fixed:
            # If in fixed mode, create a fixed GTK container and set image width and height to provided
            self.fixed_container = Gtk.Fixed()
            self.image_size = [int(n) for n in fixed.split(',')]

        # Create image
        self.image_path = image_path
        self.svg_image = Gtk.Image()
        self.svg_image.set_opacity(opacity)
        self.reload_image()

        # Add fixed container or full image
        if fixed:
            self.fixed_container.put(self.svg_image, self.image_size[2], self.image_size[3])
            self.add(self.fixed_container)
        else:
            self.add(self.svg_image)

        # Set reload interval if provided
        if reload:
            GLib.timeout_add_seconds(reload, self.reload_image)

        self.connect("draw", self.on_draw)

    def reload_image(self):
        # Reload the image
        input_stream = Gio.MemoryInputStream.new_from_data(self.get_image_data(self.image_path), None)
        pixbuf = Pixbuf.new_from_stream_at_scale(input_stream, self.image_size[0], self.image_size[1], True, None)
        self.svg_image.set_from_pixbuf(pixbuf)
        return True

    def get_image_data(self, image_path):
        if image_path.startswith('http://') or image_path.startswith('https://'):
            # If the image path is a URL, fetch it
            return bytearray(urlopen(image_path).read())
        else:
            # Else, load it from distk
            with open(image_path, 'rb') as f:
                return bytearray(f.read())

    def on_draw(self, widget, cr):
        # Handle clickthrough
        cr.set_source_rgba(0.0, 0.0, 0.0, 0.0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)
        self.input_shape_combine_region(cairo.Region(cairo.RectangleInt(0, 0, 0, 0)))

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    parser = argparse.ArgumentParser(description='Display a transparent, clickthrough SVG image overlay')
    parser.add_argument('--opacity', type=float, help='decimal; opacity of image displayed')
    parser.add_argument('--monitor', type=int, help='monitor to display overlay on')
    parser.add_argument('--fixed', type=str, help='display image in fixed region instead of scaling; provide as width,height,x,y')
    parser.add_argument('--reload', type=float, help='reload the image every specified seconds')
    parser.add_argument('image', type=str, help='path or url to SVG to display')

    args = parser.parse_args()

    win = SvgOverlay(args.image, args.fixed, args.reload, args.monitor or 0, args.opacity or .5)
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
