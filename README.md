# Sublime Function Name Display #

This plugin displays the current class and function name on the status bar in Sublime Text 2.

## Installation ##

The recommmended method of installation is via [Package Control](http://wbond.net/sublime_packages/package_control). It will download upgrades to your packages automatically.

### Package Control ###

* Follow instructions on [http://wbond.net/sublime_packages/package_control](http://wbond.net/sublime_packages/package_control)
* Install using Package Control: Install > Function Name Display package

### Using Git ###

Go to your Sublime Text 2 Packages directory and clone the repository using the command below:

git clone https://github.com/akrabat/SublimeFunctionNameDisplay "Function Name Display"


## Limitations ##

This plugin looks for Sublime's 'entity.name.type.class' and 'entity.name.function' scopes to work out where a class and function starts. Note that it doesn't determine where the class/function ends. 