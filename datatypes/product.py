from dataclasses import dataclass


@dataclass(frozen=True, order=False)
class Product:
    page_rank: int
    title: str
    image: str
    new_rank: int
    old_rank: int
    rank_percent: int
    rating: float
    total_ratings: int
    link: str
    price: list[float]
