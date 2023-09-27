from pydantic import BaseModel
from typing import List


class QuoteSchema(BaseModel):
    """ Define como um novo monitor a ser inserido deve ser representado
    """
    quote: str
    author: str




