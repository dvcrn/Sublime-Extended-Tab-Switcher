import sublime
import sublime_plugin
import os


class ViewFinder(sublime_plugin.EventListener):
    _instance = None

    def __init__(self, *args, **kwargs):
        self.__class__._instance = self
        self._listening = False

    def on_activated(self, view):
        if self._listening and view.settings().get('is_widget'):
            self._listening = False
            self.cb(view)

    @classmethod
    def instance(cls):
        if cls._instance:
            return cls._instance
        else:
            return cls()

    def start_listen(self, cb):
        self.cb = cb
        self._listening = True


class ExtendedSwitcherCommand(sublime_plugin.WindowCommand):
    # declarations
    open_files = []
    open_views = []
    window = []
    settings = []
    qpanel = None

    def quick_panel_found(self, view):
        self.qpanel = view

    # lets go
    def run(self, list_mode):
        self.group = self.window.active_group()
        self.open_files = []
        self.open_views = []
        self.window = sublime.active_window()
        self.settings = sublime.load_settings('Kirikae.sublime-settings')
        self.active_view = self.window.active_view()

        folders = self.window.folders()
        active_view_id = self.active_view.id()

        current_index = 0
        current_tab_index = 0

        for view in self.getViews(list_mode):
            current_index += 1
            is_current_view = view.id() == active_view_id

            # if skip the current active is enabled do not add the current file
            # it for selection
            if self.settings.get('skip_current_file') == True:
                if is_current_view:
                    continue

            self.open_views.append(view)  # add the view object
            file_name = view.file_name()  # get the full path
            file_path = ''

            if is_current_view:
                current_tab_index = current_index
                current_view_prefix = " (Current View)"

            else:
                current_view_prefix = ""

            if file_name:
                for folder in folders:
                    if os.path.commonprefix([folder, file_name]) == folder:
                        file_path = os.path.relpath(file_name, folder)

                if view.is_dirty():
                    # if there are any unsaved changes to the file
                    file_name += self.settings.get('mark_dirty_file_char')

                if self.settings.get('show_full_file_path') == True:
                    self.open_files.append(
                        [os.path.basename(file_name) + current_view_prefix, file_path])
                else:
                    self.open_files.append(
                        [os.path.basename(file_name) + current_view_prefix, ''])
            elif view.name():
                if view.is_dirty():
                    self.open_files.append(
                        [view.name() + self.settings.get('mark_dirty_file_char') + current_view_prefix, ''])
                else:
                    self.open_files.append(
                        [view.name() + current_view_prefix, ''])
            else:
                if view.is_dirty():
                    self.open_files.append(
                        ["Untitled" + self.settings.get('mark_dirty_file_char') + current_view_prefix, ''])
                else:
                    self.open_files.append(
                        ["Untitled" + current_view_prefix, ''])

        # Make the last item jump back
        auto_select_next_tab = self.settings.get( 'auto_select_next_tab', True )

        if current_tab_index == 1:
            current_tab_index += (0 if auto_select_next_tab else -1)

        else:
            current_tab_index -= (2 if auto_select_next_tab else 1)

        if self.check_for_sorting() == True:
            self.sort_files()

        def on_selection(selected):
            selected_view = self.open_views[selected]
            current_group = self.window.active_group()
            selected_group = self.window.get_view_index(
                self.open_views[selected])[0]
            if selected > -1:
                if current_group == selected_group:
                    self.window.focus_view(selected_view)
                else:
                    file_name = selected_view.file_name()
                    self.window.open_file(file_name,
                                          group=self.window.active_group(),
                                          flags=sublime.TRANSIENT | sublime.ENCODED_POSITION | sublime.FORCE_GROUP)


        # show the file list
        ViewFinder.instance().start_listen(self.quick_panel_found)
        self.window.show_quick_panel(self.open_files, self.tab_selected, sublime.KEEP_OPEN_ON_FOCUS_LOST, current_tab_index, on_selection)


    # display the selected open file
    def tab_selected(self, selected):
        if selected > -1:
            if self.settings.get('move_to_current_pane') == True:
                self.window.set_view_index(self.open_views[selected], self.group, 0)
                print("move pane.....")
            self.window.focus_view(self.open_views[selected])
        else:
            self.window.focus_view(self.active_view)

    # sort the files for display in alphabetical order
    def sort_files(self):
        open_files = self.open_files
        open_views = []

        open_files.sort()

        for file_path in open_files:
            file_path = file_path[0]
            for fv in self.open_views:
                if fv.file_name():
                    file_path = file_path.replace(
                        " - " + os.path.dirname(fv.file_name()), '')
                    if (file_path == os.path.basename(fv.file_name())) or (file_path == os.path.basename(fv.file_name()) + self.settings.get('mark_dirty_file_char')):
                        open_views.append(fv)
                        self.open_views.remove(fv)
                elif fv.name() == file_path or fv.name() + self.settings.get('mark_dirty_file_char') == file_path:
                    open_views.append(fv)
                    self.open_views.remove(fv)
                elif file_path == "Untitled" and not fv.name():
                    open_views.append(fv)
                    self.open_views.remove(fv)

        self.open_views = open_views

    # flags for sorting
    def check_for_sorting(self):
        if self.settings.has("sort"):
            return self.settings.get("sort", False)

    def getViews(self, list_mode):
        views = []
        # get only the open files for the active_group
        if list_mode == "active_group":
            views = self.window.views_in_group(self.window.active_group())

        # get all open view if list_mode is window or active_group doesn't have
        # any files open
        if (list_mode == "window") or (len(views) < 1):
            views = self.window.views()

        # Reverse the sorting order to make the up arrow to move right and down
        # arrow to move left
        return list(reversed(views))
