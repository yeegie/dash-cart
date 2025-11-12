from uuid import UUID


class ProductNotFound(Exception):
    def __init__(self, id: UUID = None, slug: str = None):
        self.__id = id
        self.__slug = slug
        self.details: str

        if self.__id:
            self.details = f"Product with id={self.__id} not found."
        elif self.__slug:
            self.details = f"Product with slug={self.__slug} not found."
        else:
            self.details = "Product not found."

        super().__init__(self.details)

    @property
    def id(self) -> UUID:
        return self.__id
    
    @property
    def slug(self) -> str:
        return self.__slug


class ProductAlreadyExists(Exception):
    def __init__(self, id: UUID = None, slug: str = None):
        self.__id = id
        self.__slug = slug
        self.details: str

        if self.__id:
            self.details = f"Product with id={self.__id} already exists."
        elif self.__slug:
            self.details = f"Product with slug={self.__slug} already exists."
        else:
            self.details = "Product already exists."

        super().__init__(self.details)

    @property
    def id(self) -> UUID:
        return self.__id
    
    @property
    def slug(self) -> str:
        return self.__slug


class InvalidProductId(Exception):
    pass