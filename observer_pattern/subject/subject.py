import logging
from abc import ABC
from typing import List
from ..observer.observer import Observer
from .event import Event

""" Abstract Subject class"""
class Subject(ABC):
    def __init__(self) -> None:
        self.__observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        if observer not in self.__observers:
            self.__observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self.__observers.remove(observer)
    
    def notify(self, event: Event) -> None: 
        for observer in self.__observers:
            observer.update(event)
        logging.info("Subject called notify def")
