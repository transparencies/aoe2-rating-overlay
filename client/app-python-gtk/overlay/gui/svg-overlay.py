# This file contains code from svgoverlay,
# Taken from https://gist.github.com/seigler/28dd06334b55a93692855a8dd62c1b57
# Copyright 2017-2020 Joshua Seigler.
# It's licensed under the terms of the MIT license.
#
# Modifications Copyright 2020-2020 the aoe-assoc authors.
# See COPYING.md for further legal info.

# svgoverlay
# Display an SVG from disk or URL in a fullscreen, transparent, click-through window, with settable opacity.
# When used on Arch Linux, requires AUR package python-gobject-patched for click-through functionality
#
# Example usage:
# svgoverlay --opacity 0.8 --monitor 0 filename.svg

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib


class SvgOverlay(Gtk.Window):
    # TODO: Make window resizable and svg scale in it
    # TODO: Make window draggable with mouse and lock in place with an option
    # TODO: Open options menu with a long click on the overlay

    def __init__(self, image_path, fixed, reload, monitor, opacity):
        super().__init__(self, title="svgoverlay")
        self.opacity = opacity

        self.screen = self.get_screen()
        self.visual = self.screen.get_rgba_visual()
        if self.visual is not None and self.screen.is_composited():
            self.set_visual(self.visual)

        # Move to specified monitor
        # TODO: Refactor, this is deprecated
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
