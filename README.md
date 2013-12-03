# Sublime Function Name Display

This plugin displays the current file, class and function name on the status bar in Sublime Text 2 and 3.

## Installation

The recommended method of installation is via [Package Control](https://sublime.wbond.net). It will download upgrades to your packages automatically.

### Package Control

* Follow instructions on [https://sublime.wbond.net](https://sublime.wbond.net)
* Install using Package Control: Install > Function Name Display package

### Using Git

Go to your Sublime Text Packages directory and clone the repository using the command below:

git clone https://github.com/akrabat/SublimeFunctionNameDisplay "Function Name Display"


## Limitations

This plugin looks for Sublime's 'entity.name.type.class' and 'entity.name.function' scopes to work out where a class and function starts. Note that it doesn't determine where the class/function ends. 
