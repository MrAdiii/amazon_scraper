from dataclasses import dataclass
from datatypes.product import Product


@dataclass(frozen=True, order=False)
class Department:
    department: str
    products: list[Product]
