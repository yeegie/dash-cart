# class ClientNotFound(Exception):
#     def __init__(self, id: str = None, telephone: str = None):
#         self.__id = id
#         self.__telephone = telephone
#         self.details: str

#         if self.__id:
#             self.details = f"Client with id={self.__id} not found."
#         elif self.__telephone:
#             self.details = f"Client with telephone={self.__telephone} not found."
#         else:
#             self.details = "Client not found."

#         super().__init__(self.details)

#     @property
#     def id(self) -> str:
#         return self.__id
    
#     @property
#     def telephone(self) -> str:
#         return self.__telephone


# class ClientAlreadyExists(Exception):
#     def __init__(self, id: str = None, telephone: str = None):
#         self.__id = id
#         self.__telephone = telephone
#         self.details: str

#         if self.__id:
#             self.details = f"Client with id={self.__id} already exists."
#         elif self.__telephone:
#             self.details = f"Client with telephone={self.__telephone} already exists."
#         else:
#             self.details = "Client already exists."

#         super().__init__(self.details)

#     @property
#     def id(self) -> str:
#         return self.__id
    
#     @property
#     def telephone(self) -> str:
#         return self.__telephone


class InvalidPhoneNumber(Exception):
    def __init__(self, details: str, telephone: str | None = None):
        self._telephone = telephone
        self.details = details

class InvalidCode(Exception):
    def __init__(self, details: str, telephone: str | None = None, entered_code: str | None = None):
        self._telephone = telephone
        self._entered_code = entered_code
        self.details = details

class InvalidToken(Exception):
    def __init__(self, details: str, token: str | None = None):
        self._token = token
        self.details = details


# class CodeExpired(Exception):
#     pass
