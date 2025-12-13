from abc import ABC, abstractmethod


class Entity(ABC):
    @abstractmethod
    def input(self):
        """Input entity information"""
        pass

    @abstractmethod
    def list(self):
        """Display entity information"""
        pass
