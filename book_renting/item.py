from dataclasses import dataclass, field
from book_renting.random_number_utils import RandomUtils

@dataclass(frozen=True, order=True, slots=True)
class Item:
    name: str
    author: str
    type: str
    _age_rating: int
    id: str = field(default_factory=RandomUtils.generate_random_id)

    @property
    def search_string(self):
        return f"{self.name} - {self.author} {self.type} {self._age_rating}"