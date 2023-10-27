from typing import Optional, List

from fastapi import FastAPI
from lfortune.abstract.fortune_source import FortuneSource
from pydantic import BaseModel

from .functions import get_result, get_fortune


VERSION = '0.5'


class InputFortuneSource(BaseModel):
    path: str
    probability: Optional[int] = None


class InputFortunesSources(BaseModel):
    sources: List[InputFortuneSource]


api = FastAPI(
    title="Fortune API",
    version=VERSION,
)


@api.get("/")
async def api_get_fortune(explore: bool = False) -> dict | list:
    return get_result('', None, explore)


@api.get("/{path:path}/{index:int}")
async def api_get_fortune_path_index(path: str, index: int) -> dict:
    return get_result(path, index, False)


@api.get("/{path:path}")
async def api_get_fortune_path(path: str, explore: bool = False, index: int = None) -> dict | list:
    return get_result(path, index, explore)


@api.post("/")
async def api_post_fortune_path(input_sources: InputFortunesSources) -> dict:
    sources = []
    for s in input_sources.sources:
        sources.append(FortuneSource(s.path, s.probability or 0))
    return get_fortune(sources)
