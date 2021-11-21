from abc import ABC, abstractmethod
from app_state import AppState
from tkinter import Tk


class Screen(ABC):

    def __init__(self, app_root: Tk, app_state: AppState):
        self.app_root = app_root
        self.app_state = app_state

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def destroy(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @staticmethod
    def name():
        return None
