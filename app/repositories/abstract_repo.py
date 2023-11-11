from abc import ABC, abstractmethod


class AbstractRepository(ABC):

     @abstractmethod
     async def add(self):
          raise NotImplemented

     @abstractmethod
     async def get_one(self):
          raise NotImplemented

     @abstractmethod
     async def get_list(self):
          raise NotImplemented

     @abstractmethod
     async def update(self):
          raise NotImplemented

     @abstractmethod
     async def delete(self):
          raise NotImplemented