from typing import Annotated

from fastapi import Query, Depends

from pydantic import BaseModel


class Paginator(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, le=20)]


paginator = Annotated[Paginator, Depends()]
