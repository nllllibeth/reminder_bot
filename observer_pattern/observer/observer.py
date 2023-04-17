from abc import ABC, abstractmethod

""" Abstract Observer class"""
class Observer(ABC):
    @abstractmethod
    def update(self, event, bot):
        pass 
