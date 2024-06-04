from typing import List, Union

from pydantic import BaseModel


class WebSearchResult(BaseModel):
    title: str
    """The title of the search result."""

    link: str
    """The link to the search result."""

    snippet: str
    """The snippet of the search result."""


class WebSearchImageResult(BaseModel):
    title: str
    """The title of the image search result."""

    link: str
    """The link to the image search result."""

    size: str
    """The size of the image search result."""

    context: str
    """The context of the image search result."""

    byteSize: str
    """The byte size of the image search result."""

    mime: str
    """The MIME type of the image search result."""


WebSearchResponses = List[WebSearchResult]
WebSearchImageResponses = List[WebSearchImageResult]


EitherWebSearchResponses = Union[WebSearchResponses, WebSearchImageResponses]

# TODO: Remake web search api format on API side to have a consistent formatting throughout
# both DDG and Google search APIs including both general web search and image search.
