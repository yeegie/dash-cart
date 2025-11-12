__all__ = ["IOC"]

from typing import Generic, Type, TypeVar

T = TypeVar("T")


class IOC:
    """
    ### IoC Container
    Store dependencies by key-value principe

    @example

    Store dependencie
    ``` python
    container.attach("notificator", notificator)
    ```

    Get from container
    ``` python
    notificator = container.get("notificator")
    ```
    """

    def __init__(self) -> None:
        self._container = {}

    def set(self, key: Type[T], instance: T) -> None:
        if not isinstance(instance, key):
            raise TypeError(f"Instance [{key}] must be type of [{key}]")

        self._container[key] = instance

    def get(self, key: Type[T]) -> T:
        if key not in self._container.keys():
            raise ValueError(f"Key[{key}] not found.")

        instance = self._container[key]

        if not isinstance(instance, key):
            raise TypeError(f"Stored instance is not type of {key}")

        return instance

    def __str__(self) -> str:
        return f"Container: {self._container}"