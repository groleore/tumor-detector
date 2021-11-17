from tkinter import (
    filedialog, Tk, Menu, Label, StringVar, ttk, Button
)
from PIL import ImageTk
from const import *

from app_state import AppState


class App:
    def __init__(self):
        self.app_state = AppState()
        self._init_app()

        self._render_menu()
        self._render_main_screen()

    def _init_app(self):
        self.root = Tk()

        self.root.title('{} v.{}'.format(APP_TITLE, APP_VERSION))
        self.root.geometry('{}x{}'.format(SCREEN_WIDTH, SCREEN_HEIGHT))

        self.root.bind('<Left>', lambda event: self.prev())
        self.root.bind('<Right>', lambda event: self.next())

        self.canvas = None
        self.file_string = StringVar()
        self.previews: list = []

    def _render_menu(self):
        menu_bar = Menu(self.root)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open Single File", command=self.open_file)
        file_menu.add_command(label="Open Folder", command=self.open_folder)
        menu_bar.add_cascade(label="File", menu=file_menu)

        self.root.config(menu=menu_bar)

    def _render_main_screen(self):
        self._render_previews()
        self._render_controls()
        self._render_canvas()

    def _render_controls(self):
        control_frame = ttk.Frame(self.root)

        btn = Button(control_frame, text='<', command=self.prev)
        btn.pack(side='left')

        file_label = Label(control_frame, textvariable=self.file_string)
        file_label.pack(side='left')

        btn = Button(control_frame, text='>', command=self.next)
        btn.pack(side='left')

        control_frame.pack(side='top')

    def _render_previews(self):
        preview_frame = ttk.Frame(self.root)

        self.previews = [Label(preview_frame) for _ in range(PREVIEW_IMAGES_NUMBER)]
        for idx, preview in enumerate(self.previews):
            preview.bind('<Button-1>', self.go_to(idx))
            preview.pack(side='left')

        preview_frame.pack(side='top')

    def _render_canvas(self):
        self.canvas = Label(self.root)
        self.canvas.pack(side="top", expand=1)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=SUPPORTED_FORMATS_MASK, title=OPEN_FILE_TIP)
        self._handle_event(EVENT_OPEN_FILE, file_path)

    def open_folder(self):
        dir_path = filedialog.askdirectory(title=OPEN_DIR_TIP)
        self._handle_event(EVENT_OPEN_DIR, dir_path)

    def next(self):
        self._handle_event(EVENT_NEXT)

    def prev(self):
        self._handle_event(EVENT_PREVIOUS)

    def go_to(self, go_to_index):
        return lambda event: self._handle_event(EVENT_GO_TO, go_to_index)

    def _handle_event(self, name, *args, **kwargs):
        self.app_state.emit(name, *args, **kwargs)
        self._update()

    def _update_image(self):
        tk_image = ImageTk.PhotoImage(self.app_state.current_image)
        self.canvas.configure(image=tk_image)
        self.canvas.image = tk_image

    def _update_file_position(self):
        current, total = self.app_state.file_position
        pos = '{} of {}'.format(current, total) if current else ''
        self.file_string.set(pos)

    def _update_preview(self):
        preview_images = self.app_state.previews
        for idx in range(len(self.previews)):
            preview_label = self.previews[idx]
            preview_image = preview_images[idx] if len(preview_images) > idx else None
            tk_image = ImageTk.PhotoImage(preview_image) if preview_image else None
            preview_label.configure(image=tk_image)
            preview_label.image = tk_image

    def _update(self):
        self._update_image()
        self._update_preview()
        self._update_file_position()

    def run(self):
        self.root.mainloop()
