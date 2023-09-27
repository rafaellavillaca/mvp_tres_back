from pydantic import BaseModel
from typing import List


class FunFactSchema(BaseModel):
    """ Define como um novo monitor a ser inserido deve ser representado
    """
    fun_fact: str




