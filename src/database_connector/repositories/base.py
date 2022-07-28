import abc


class BaseRepository(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def create(self):
        return

    @staticmethod
    @abc.abstractmethod
    def delete(self):
        return

    @staticmethod
    @abc.abstractmethod
    def update(self):
        return
