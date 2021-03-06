import gi

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Gedit', '3.0')

from gi.repository import GObject, Gdk, Gtk, Gedit
class CutLineWindowActivatable(GObject.Object, Gedit.WindowActivatable):

  window = GObject.property(type=Gedit.Window)

  def __init__(self):
    GObject.Object.__init__(self)

  def do_activate(self):
    self._handler_id = self.window.connect('key-press-event', self.on_key_press)

  def do_deactivate(self):
    self.window.disconnect(self._handler_id)

  def on_key_press(self, term, event):
    if event.keyval in (Gdk.KEY_C, Gdk.KEY_c):
      modifiers = event.state & Gtk.accelerator_get_default_mod_mask()

      if modifiers == Gdk.ModifierType.CONTROL_MASK:
        self.copy_line()

    return False

  def copy_line(self):
    doc = self.window.get_active_document()
    selection_iter = doc.get_selection_bounds()

    if len(selection_iter) == 0:
      view = self.window.get_active_view()
      insert = doc.get_insert()

      itstart = doc.get_iter_at_mark(insert)
      offset = itstart.get_line_offset()
      itstart.set_line_offset(0)
      itend = doc.get_iter_at_mark(insert)
      itend.forward_line()
      doc.begin_user_action()
      doc.select_range(itstart, itend)
      view.copy_clipboard()
      itstart = doc.get_iter_at_mark(insert)
      itstart.set_line_offset(offset)
      doc.end_user_action()
      doc.place_cursor(itstart)
