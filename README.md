Kirikae for Sublime Text
==================================================

Fork of https://github.com/rajeshvaya/Sublime-Extended-Tab-Switcher since that seems pretty inactive

This plugin is for quickly switching to a given open tab. Tabs will be treated as buffers: It shouldn't matter in which window/group they are, switching should be easy.


## Key Bindings

* On pressing `ctrl+alt+w` show all tabs inside the current window
* On pressing `ctrl+alt+s` show all tabs inside the current split

User can change the default key binding at `Preferences -> Package Settings -> Kiriake -> Key Bindings - User`


## Configurations
User can overwrite the following configurations by adding flags in the User - Settings section which can be access by `Preferences -> Package Settings -> Kirikae -> Settings - User`

* Sorting

	By default the the files are sorted in the order of "open files" in the side bar. To enable the sorting the user can change the defauly key binding and adding the following flag in the settings

	```javascript
	{
		"sort": "true"
	}
	```

* Skip current file

	By default the current active file/view is also displayed within the selection of the open files. This can be overwritten by adding the following flag in the settings

	```javascript
	{
		"skip_current_file": "true"
	}
	```


* Mark dirty file

	By default all the dirty/unsaved files are marked with "*". This can be overwritten by adding the following flag in the settings


	Tip: This character can be also use to view all the unsaved files while searching the open files


	```javascript
	{
		"mark_dirty_file_char": "<your-char>"
	}

	```

* Show full file path

	By default the files listed will contain only the filename, This can be overwritten by adding the following flag in the settings

	```javascript
	{
		"show_full_file_path": true
	}

	```

* Open tabs in the current pane

	By default, selecting a file will focus its view in its current position. When the following flag is set to true, the view will be moved into the currently active pane.

	```javascript
	{
		"move_to_current_pane": false
	}

	```

## Credits

David Mohl - [@dvcrn](https://github.com/dvcrn)

Rajesh Vaya - [@rajeshvaya](https://github.com/rajeshvaya)

Kohichi Aoki - [@drikin](https://github.com/drikin)

Philip Oliver - [@phildopus](https://github.com/phildopus)

Rrg - [@rrg](https://github.com/rrg)


## License

MIT
