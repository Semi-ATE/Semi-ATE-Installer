from dataclasses import dataclass, fields
from typing import List


@dataclass
class BaseDataClass:
    @classmethod
    def get_fields(cls) -> List[str]:
        return [getattr(cls, field.name) for field in fields(cls)]
