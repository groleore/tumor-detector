from tkinter import (
    filedialog, Tk, Menu, messagebox
)
from const import *

from app_state import AppState
from screen_factory import get_screen


class App:
    def __init__(self):
        self.app_state: AppState = AppState()
        self.screen = None

        self._init_app()
        self._render_menu()

    def _init_app(self):
        self.app_root = Tk()

        self.app_root.title('{} v.{}'.format(APP_TITLE, APP_VERSION))
        self.app_root.geometry('{}x{}'.format(SCREEN_WIDTH, SCREEN_HEIGHT))

    def _render_menu(self):
        menu_bar = Menu(self.app_root)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open Single File", command=self.open_file)
        file_menu.add_command(label="Open Folder", command=self.open_folder)
        menu_bar.add_cascade(label="File", menu=file_menu)

        self.app_root.config(menu=menu_bar)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=SUPPORTED_FORMATS_MASK, title=OPEN_FILE_TIP)
        try:
            self._handle_event(EVENT_OPEN_FILE, file_path)
            self._set_screen(DISPLAY_SCREEN)
        except Exception as e:
            messagebox.showerror('Error on open file', str(e))

    def open_folder(self):
        dir_path = filedialog.askdirectory(title=OPEN_DIR_TIP)

        try:
            self._handle_event(EVENT_OPEN_DIR, dir_path)
            self._set_screen(DISPLAY_SCREEN)
        except Exception as e:
            messagebox.showerror('Error on open folder', str(e))

    def _handle_event(self, name, *args, **kwargs):
        self.app_state.emit(name, *args, **kwargs)
        self._update()

    def _set_screen(self, screen_name):
        if self.screen and self.screen.name() == screen_name:
            return

        if self.screen is not None:
            self.screen.destroy()

        self.screen = get_screen(screen_name)(self.app_root, self.app_state)
        self.screen.render()

    def _update(self):
        if self.screen:
            self.screen.update()

    def run(self):
        self.app_root.mainloop()
