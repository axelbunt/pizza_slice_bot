from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    username: str
    cart: dict
    index_of_current_item_in_view: int
    is_banned: bool

    def __init__(
        self,
        user_id: int,
        username: str,
        cart=None,
        index_of_current_item_in_view: int = 0,
        is_banned: bool = False,
    ) -> None:
        if cart is None:
            cart = {}
        self.user_id = user_id
        self.username = username
        self.cart = cart
        self.index_of_current_item_in_view = index_of_current_item_in_view
        self.is_banned = is_banned
