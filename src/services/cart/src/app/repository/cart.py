from .IRepository import IRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, delete
from app.repository.scheams.cart import CartSchema, GetCartSchema, GetCartsSchema, CartItemSchema
from app.repository.models.Cart import Cart
from app.repository.models.CartItem import CartItem
import logging
from uuid import UUID
from typing import Optional


class CartRepository(IRepository):
    def __init__(self, session: AsyncSession, logger: logging.Logger):
        self.__session = session
        self.__logger = logger

    async def create(self, cart: CartSchema) -> GetCartSchema:
        new_cart = Cart(user_id=cart.user_id)

        for item in cart.items:
            cart_item = CartItem(
                item_number=item.item_number,
                quantity=item.quantity
            )
            new_cart.items.append(cart_item)

        try:
            self.__session.add(new_cart)
            await self.__session.commit()
            await self.__session.refresh(new_cart)
        except Exception as ex:
            self.__logger.error(f"CART CREATION ERROR: {ex}")

        return GetCartSchema(**new_cart.to_dict())

    async def get_by_id(self, id: UUID) -> Optional[GetCartSchema]:
        result = await self.__session.execute(
            select(Cart)
            .where(Cart.id == id)
        )

        result = result.scalar_one_or_none()

        if result is None:
            return None
        
        return GetCartSchema(**result.to_dict())
    

    async def get_by_user_id(self, user_id: UUID) -> Optional[GetCartSchema]:
        result = await self.__session.execute(
            select(Cart)
            .where(Cart.user_id == user_id)
        )

        result = result.scalar_one_or_none()

        if result is None:
            return None
        
        return GetCartSchema(**result.to_dict())


    async def update(self, user_id, cart: CartSchema) -> bool:
        old_cart = await self.get_by_user_id(user_id)
        if not old_cart:
            return False

        if hasattr(cart, 'items') and cart.items is not None:
            old_cart.items.clear()
            for item in cart.items:
                old_cart.items.append(
                    CartItem(
                        item_number=item.item_number,
                        quantity=item.quantity
                    )
                )

        try:
            await self.__session.commit()
            await self.__session.refresh(old_cart)
            self.__logger.info(f"Cart updated for user_id={user_id}")
            return True
        except SQLAlchemyError as ex:
            await self.__session.rollback()
            self.__logger.error(f"Cart update failed for user_id={user_id}: {ex}")
            return False

    async def add_item(self, user_id: UUID, item_number: str) -> GetCartSchema:
        pass

    async def remove_item(self, user_id: UUID, item_number: str) -> GetCartSchema:
        pass

    async def delete(self, id: UUID) -> bool:
        try:
            result = await self.__session.execute(
                delete(Cart)
                .where(Cart.id == id)
            )
            await self.__session.commit()
            return result.rowcount > 0  # Return True if deleted
        except SQLAlchemyError as ex:
            self.__logger.error(f"An error occurred during deletion cart: {ex}")
            await self.__session.rollback()
            return False

    async def list(self) -> GetCartsSchema:
        try:
            result = await self.__session.execute(
                select(Cart))
            carts = result.scalars().all()
            carts_schemas = [GetCartSchema(**cart.to_dict()) for cart in carts]
            return GetCartsSchema(carts=carts_schemas)
        except SQLAlchemyError as ex:
            self.__logger.error(f"Failed to retrieve the cart list: {ex}")
            return GetCartsSchema(products=[])
