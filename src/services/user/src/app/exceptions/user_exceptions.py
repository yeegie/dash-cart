class UserNotFound(Exception):
    def __init__(self, id: str = None, telephone: str = None):
        self.__id = id
        self.__telephone = telephone
        self.details: str

        if self.__id:
            self.details = f"User with id={self.__id} not found."
        elif self.__telephone:
            self.details = f"User with telephone={self.__telephone} not found."
        else:
            self.details = "User not found."

        super().__init__(self.details)

    @property
    def id(self) -> str:
        return self.__id
    
    @property
    def telephone(self) -> str:
        return self.__telephone


class UserAlreadyExists(Exception):
    def __init__(self, id: str = None, telephone: str = None):
        self.__id = id
        self.__telephone = telephone
        self.details: str

        if self.__id:
            self.details = f"User with id={self.__id} already exists."
        elif self.__telephone:
            self.details = f"User with telephone={self.__telephone} already exists."
        else:
            self.details = "User already exists."

        super().__init__(self.details)

    @property
    def id(self) -> str:
        return self.__id
    
    @property
    def telephone(self) -> str:
        return self.__telephone


class InvalidPhoneNumber(Exception):
    pass


class InvalidEmail(Exception):
    pass
