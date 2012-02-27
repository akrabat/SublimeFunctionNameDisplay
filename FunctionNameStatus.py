
import sublime, sublime_plugin, time

# Ideas taken from C0D312, nizur & tito in http://www.sublimetext.com/forum/viewtopic.php?f=2&t=4589

s = sublime.load_settings('Function Name Display.sublime-settings')

class Pref:
  def load(self):
    Pref.display_class = s.get('display_class', True)
    Pref.display_function = s.get('display_function', True)
    Pref.wait_time = 0.02
    Pref.time = time.time()

Pref().load()
s.add_on_change('display_class', lambda:Pref().load())
s.add_on_change('display_function', lambda:Pref().load())

class FunctionNameStatusEventHandler(sublime_plugin.EventListener):

  # Event handlers
  def on_selection_modified(self, view):
    now = time.time()
    if now - Pref.time > Pref.wait_time:
      Pref.time = now
      self.display_current_class_and_function(view)
    else:
      Pref.time = now

  # display the current class and function name
  def display_current_class_and_function(self, view):
    if view.settings().get('is_widget'):
      return

    region = view.sel()[0]
    region_row, region_col = view.rowcol(region.begin())

    s = ""
    found = False

    # Look for any classes
    if Pref.display_class:
      class_regions = view.find_by_selector('entity.name.type.class')
      for r in reversed(class_regions):
        row, col = view.rowcol(r.begin())
        if row <= region_row:
          s = view.substr(r)
          found = True
          if Pref.display_function:
            s += "::"
          break;
    
    # Look for any functions including PHP magic functions
    if Pref.display_function:
      function_regions = view.find_by_selector('entity.name.function') + view.find_by_selector('support.function.magic.php')
      if function_regions:
        function_regions.sort()
        for r in reversed(function_regions):
          row, col = view.rowcol(r.begin())
          if row <= region_row:
            s = s + view.substr(r)
            found = True
            break

    if not found:
      view.erase_status('function')
    else:
      view.set_status('function', s)
