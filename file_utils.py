from pathlib import Path
from pydicom import dcmread
from PIL import Image
from const import PREVIEW_IMAGE_WIDTH, COLOR_RED, SELECTED_PREVIEW_BORDER, RGB_COLOR_MODE


def read_files_from_dir(dir_path, supported_formats=None, recursive=False):
    file_list = []
    return _read_files_from_dir(file_list, dir_path, supported_formats, recursive)


def _read_files_from_dir(file_list, dir_path, supported_formats, recursive):
    root_dir = Path(dir_path)

    for file in root_dir.iterdir():
        if file.is_file():
            if not supported_formats or file.suffix in supported_formats:
                file_list.append(file)
        else:
            if recursive:
                _read_files_from_dir(file_list, dir_path, supported_formats, recursive)

    return file_list


def read_dcm_image(img_path):
    ds = dcmread(img_path)
    return Image.fromarray(ds.pixel_array)


def read_dcm_image_as_preview(img_path):
    img = read_dcm_image(img_path)
    base_width, base_height = img.size

    scale_c = (PREVIEW_IMAGE_WIDTH / float(base_width))
    new_height = int((float(base_height) * float(scale_c)))

    img = img.resize((PREVIEW_IMAGE_WIDTH, new_height), Image.ANTIALIAS)

    return img


def add_border_to_image(img, border_size=SELECTED_PREVIEW_BORDER, color=COLOR_RED):
    background = Image.new(RGB_COLOR_MODE, (img.width + border_size, img.height + border_size), color)
    converted_img = img.convert(RGB_COLOR_MODE)
    half_border = int(border_size / 2.0)
    background.paste(converted_img, (half_border, half_border))
    return background
