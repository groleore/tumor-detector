from const import SUPPORTED_FORMATS, PREVIEW_IMAGES_NUMBER
from file_utils import (
    read_files_from_dir,
    read_dcm_image,
    read_dcm_image_as_preview,
    add_border_to_image,
)
from event_emitter import EventEmitter
from singleton import Singleton


class AppState(EventEmitter, metaclass=Singleton):

    def __init__(self):
        super().__init__()

        self.file_list: list = []
        self.current_image = None
        self.previews: list = []
        self.index: int = -1

    def _handle_next(self, *args, **kwargs):
        if self._is_next_enabled():
            self.index += 1
            self._update_image_position()

    def _handle_prev(self, *args, **kwargs):
        if self._is_prev_enabled():
            self.index -= 1
            self._update_image_position()

    def _handle_open_file(self, *args, **kwargs):
        file_path = args[0]
        if not file_path:
            return

        self.file_list = [file_path]
        self._process_new_file_list()

    def _handle_open_dir(self, *args, **kwargs):
        dir_path = args[0]
        if not dir_path:
            return

        self.file_list = read_files_from_dir(dir_path, SUPPORTED_FORMATS)
        self._process_new_file_list()

    def _process_new_file_list(self):
        if len(self.file_list) == 0:
            return

        self.index = 0
        self.all_previews = [read_dcm_image_as_preview(f) for f in self.file_list]
        self._update_image_position()

    def _handle_go_to(self, *args, **kwargs):
        go_to_index = args[0]
        new_index = self.index - self.index % PREVIEW_IMAGES_NUMBER + go_to_index
        if new_index < len(self.file_list):
            self.index = new_index
            self._update_image_position()

    def _read_current_image(self):
        self.current_image = read_dcm_image(self.current_file)

    def _calculate_previews(self):
        start_index = self.index - self.index % PREVIEW_IMAGES_NUMBER
        end_index = start_index + min(PREVIEW_IMAGES_NUMBER, len(self.file_list) - start_index)

        selected = self.index % PREVIEW_IMAGES_NUMBER
        previews = self.all_previews[start_index:end_index]

        previews[selected] = add_border_to_image(previews[selected])
        return previews

    def _is_next_enabled(self):
        return -1 < self.index < len(self.file_list) - 1

    def _is_prev_enabled(self):
        return self.index > 0

    def _update_image_position(self):
        try:
            self._read_current_image()
            self.previews = self._calculate_previews()
        except Exception as e:
            print(e)
            self.error = str(e)

    @property
    def current_file(self):
        if self.file_list:
            return str(self.file_list[self.index])
        raise Exception('No current file')

    @property
    def file_position(self):
        if self.file_list:
            return self.index + 1, len(self.file_list)
        return 0, 0
