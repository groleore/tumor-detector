from tkinter import (
    Label, ttk, Button, StringVar, Tk
)
from PIL import ImageTk
from const import *
from screens.screen import Screen


class DisplayScreen(Screen):

    def __init__(self, app_root: Tk, app_state):
        super().__init__(app_root, app_state)

        self.canvas = None
        self.file_string = StringVar()
        self.previews: list = []
        self.image_frame = ttk.Frame(self.app_root)

    def render(self):
        self._render_previews()
        self._render_controls()
        self._render_canvas()

        self.image_frame.pack(side='left', fill='y', padx=50, pady=20)

        self.app_root.bind('<Left>', lambda event: self._prev())
        self.app_root.bind('<Right>', lambda event: self._next())

        self.update()

    def destroy(self):
        self.image_frame.destroy()
        self.app_root.unbind('<Right>')
        self.app_root.unbind('<Left>')

    def update(self):
        self._update_image()
        self._update_preview()
        self._update_file_position()

    @staticmethod
    def name():
        return DISPLAY_SCREEN

    def _render_controls(self):
        control_frame = ttk.Frame(self.image_frame)

        btn = Button(control_frame, text='<', command=self._prev)
        btn.pack(side='left')

        file_label = Label(control_frame, textvariable=self.file_string)
        file_label.pack(side='left')

        btn = Button(control_frame, text='>', command=self._next)
        btn.pack(side='left')

        control_frame.pack(side='top')

    def _render_previews(self):
        preview_frame = ttk.Frame(self.image_frame)

        self.previews = [Label(preview_frame) for _ in range(PREVIEW_IMAGES_NUMBER)]
        for idx, preview in enumerate(self.previews):
            preview.bind('<Button-1>', self._go_to(idx))
            preview.pack(side='left')

        preview_frame.pack(side='top')

    def _render_canvas(self):
        self.canvas = Label(self.image_frame)
        self.canvas.pack(side="top", expand=1)

    def _next(self):
        self._handle_event(EVENT_NEXT)

    def _prev(self):
        self._handle_event(EVENT_PREVIOUS)

    def _go_to(self, go_to_index):
        return lambda event: self._handle_event(EVENT_GO_TO, go_to_index)

    def _handle_event(self, name, *args, **kwargs):
        self.app_state.emit(name, *args, **kwargs)
        self.update()

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
