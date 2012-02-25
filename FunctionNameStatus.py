
import sublime, sublime_plugin
from random import randrange

# Ideas taken from C0D312, nizur & tito in http://www.sublimetext.com/forum/viewtopic.php?f=2&t=4589
# Also, waiting concept is from facelessuser in http://www.sublimetext.com/forum/viewtopic.php?f=6&t=4960

class FunctionNameStatusEventHandler(sublime_plugin.EventListener):

  def __init__(self):
    self.wait_time = 100
    self.wait_id = None

  # Event handlers
  def on_selection_modified(self, view):
    self.view = view
    self.wait_ms = self.wait_time
    self.wait()

  def on_deactivated(self, view):
    view.erase_status('function')

  def on_close(self, view):
    view.erase_status('function')

  def on_activated(self, view):
     self.display_current_class_and_function(view)
      
  # display the current class and function name
  def display_current_class_and_function(self, view):
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


  # wait methods so that we don't make ST2 crawl
  def check_wait(self, wait_id):
    if self.wait_id != wait_id:
      new_wait_id = randrange(1, 999999)
      self.wait_id = new_wait_id
      sublime.set_timeout(
        lambda: self.check_wait(wait_id=new_wait_id),
        self.wait_ms
      )
    else:
      self.wait_id = None
      self.display_current_class_and_function(self.view)

  def wait(self):
      new_wait_id = randrange(1, 999999)
      if self.wait_id == None:
          self.wait_id = new_wait_id
          sublime.set_timeout(
              lambda: self.check_wait(wait_id=new_wait_id),
              self.wait_ms
          )
      else:
          self.wait_id = new_wait_id
