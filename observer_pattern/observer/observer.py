import logging
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, event, bot):
        logging.info("Observer called notify def")
        pass 