
import sublime, sublime_plugin, time

# Ideas taken from C0D312, nizur & tito in http://www.sublimetext.com/forum/viewtopic.php?f=2&t=4589

class FunctionNameStatusEventHandler(sublime_plugin.EventListener):

  def __init__(self):
    self.wait_time = 0.02
    self.time = time.time()

  # Event handlers
  def on_selection_modified(self, view):
    now = time.time()
    if now - self.time > self.wait_time:
      self.time = now
      self.display_current_class_and_function(view)
    else:
      self.time = now

  def on_deactivated(self, view):
    view.erase_status('function')

  def on_close(self, view):
    view.erase_status('function')

  def on_activated(self, view):
     self.display_current_class_and_function(view)
      
  # display the current class and function name
  def display_current_class_and_function(self, view):
    if view.settings().get('is_widget'):
      return

    region = view.sel()[0]
    region_row, region_col = view.rowcol(region.begin())

    # Look for any classes
    s = ""
    class_regions = view.find_by_selector('entity.name.type.class')
    for r in reversed(class_regions):
      row, col = view.rowcol(r.begin())
      if row <= region_row:
        s = view.substr(r) + "::"

    # Look for any functions including PHP magic functions
    function_regions = view.find_by_selector('entity.name.function') + view.find_by_selector('support.function.magic.php')
    if not function_regions:
      view.erase_status('function')
      return

    function_regions.sort()
    for r in reversed(function_regions):
      row, col = view.rowcol(r.begin())
      if row <= region_row:
        s = s + view.substr(r)
        view.set_status('function', s)
        return

    view.erase_status('function')
