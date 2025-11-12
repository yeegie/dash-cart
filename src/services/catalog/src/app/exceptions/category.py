from uuid import UUID


class CategoryNotFound(Exception):
    def __init__(self, id: UUID | None = None, slug: str | None = None):
        self._id = id
        self._slug = slug

        if self._id:
            self.details = f"Category with id={self._id} not found."
        elif self._slug:
            self.details = f"Category with slug={self._slug} not found."
        else:
            self.details = "Category not found."

        super().__init__(self.details)

    @property
    def id(self) -> UUID | None:
        return self._id

    @property
    def slug(self) -> str | None:
        return self._slug


class CategoryAlreadyExists(Exception):
    def __init__(self, id: UUID | None = None, slug: str | None = None):
        self._id = id
        self._slug = slug

        if self._id:
            self.details = f"Category with id={self._id} already exists."
        elif self._slug:
            self.details = f"Category with slug={self._slug} already exists."
        else:
            self.details = "Category already exists."

        super().__init__(self.details)

    @property
    def id(self) -> UUID | None:
        return self._id

    @property
    def slug(self) -> str | None:
        return self._slug


class InvalidCategoryId(Exception):
    pass