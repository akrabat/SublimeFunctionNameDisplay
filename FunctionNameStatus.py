
import sublime, sublime_plugin, thread, re
from time import time, sleep

# Ideas taken from C0D312, nizur & tito in http://www.sublimetext.com/forum/viewtopic.php?f=2&t=4589

s = sublime.load_settings('Function Name Display.sublime-settings')

class Pref:
  def load(self):
    Pref.display_class     = s.get('display_class', False)
    Pref.display_function  = s.get('display_function', True)
    Pref.display_arguments = s.get('display_arguments', False)
    Pref.wait_time         = 0.12
    Pref.time              = time()
    Pref.modified          = False

Pref = Pref()
Pref.load()
s.add_on_change('reload', lambda:Pref.load())

clean_name = re.compile('^\s*(public\s+|private\s+|protected\s+|static\s+|function\s+|def\s+)+', re.I)


class FunctionNameStatusEventHandler(sublime_plugin.EventListener):

  def on_load(self, view):
    Pref.time = time()
    Pref.modified = True
    view.settings().set('function_name_status_row', -1)
    sublime.set_timeout(lambda:self.display_current_class_and_function(view, 'on_load'), 0)

  def on_modified(self, view):
    Pref.time = time()
    Pref.modified = True

  # Event handlers
  def on_selection_modified(self, view):
    now = time()
    if now - Pref.time > Pref.wait_time:
      Pref.time = now
      Pref.modified = False
      sublime.set_timeout(lambda:self.display_current_class_and_function(view, 'on_selection_modified'), 0)
    else:
      Pref.modified = True
      Pref.time = now

  # display the current class and function name
  def display_current_class_and_function(self, view, where):
    view_settings = view.settings()
    if view_settings.get('is_widget'):
      return

    for region in view.sel():
      region_row, region_col = view.rowcol(region.begin())

      if region_row != view_settings.get('function_name_status_row', -1):
        view_settings.set('function_name_status_row', region_row)
      else:
        return

      # print 'running from '+where

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
            break;

      # Look for any functions
      if Pref.display_function:
        function_regions = view.find_by_selector('meta.function')
        if function_regions:
          for r in reversed(function_regions):
            row, col = view.rowcol(r.begin())
            if row <= region_row:
              if Pref.display_class and s:
                s += "::"
              lines = view.substr(r).splitlines()
              name = clean_name.sub('', lines[0])
              if Pref.display_arguments:
                s += name.strip()
              else:
                if 'C++' in view.settings().get('syntax'):
                  if Pref.display_class:
                    s += name.split('(')[0].strip()
                  else:
                    s += name.split('(')[0].split('::')[1].strip()
                else:
                  s += name.split('(')[0].split(':')[0].strip()
              found = True
              break

      if not found:
        view.erase_status('function')
      else:
        view.set_status('function', s)
      return
    view.erase_status('function')

function_name_run_call = FunctionNameStatusEventHandler().display_current_class_and_function
def function_name_run():
    Pref.modified = False
    Pref.time = time()
    window = sublime.active_window()
    view = window.active_view() if window != None else None
    if view:
      function_name_run_call(view, 'thread')

def function_name_loop():
    while True:
        if Pref.modified == True and time() - Pref.time > Pref.wait_time:
            sublime.set_timeout(lambda: function_name_run(), 0)
        sleep(0.5)

if not 'running_function_name_loop' in globals():
    running_function_name_loop = True
    thread.start_new_thread(function_name_loop, ())
