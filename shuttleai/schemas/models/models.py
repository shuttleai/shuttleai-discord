from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, RootModel

from shuttleai.schemas.models.capabilities import Capabilities


class ProxyType(str, Enum):
    proxy = "proxy"


class ModelType(str, Enum):
    model = "model"


class BaseModelCard(BaseModel):
    id: str
    """The ID of the model object."""
    object: ModelType = ModelType.model
    """The object type, which is always "model" for a model object."""
    created: int
    """The Unix timestamp when the model was created."""
    owned_by: str
    """The organization ID of the owner of the model."""
    cost: int = 1
    """The usage cost per request to this model."""
    premium: bool = False
    """Whether the model requires premium permissions."""
    endpoint: Union[str, List[str]]
    """The endpoint URL(s) for the model."""


class VerboseModelCard(BaseModelCard):
    name: str
    """The pretty name of the model."""
    description: str
    """The description of the model."""
    maintenance: Optional[bool] = None
    """Whether the model is under maintenance. If true, the model is not available for use."""
    beta: Optional[bool] = None
    """Whether the model is in beta. If true, the model may have unstable behavior and must be requested to use."""
    capabilities: Optional[Capabilities] = None
    """The capabilities of the model."""


class ProxyCard(BaseModel):
    id: str
    """The ID of the proxy object."""
    object: ProxyType = ProxyType.proxy
    """The object type, which is always "proxy" for a proxy object."""
    proxy_to: str
    """The model ID that the proxy points to."""

    @property
    def parent(self) -> BaseModelCard:
        """The parent model card that the proxy points to."""
        return f"tmp-{self.proxy_to}"

    @parent.setter
    def parent(self, value: BaseModelCard):
        self._parent = value


ListModelsData = List[Union[BaseModelCard, ProxyCard]]


ListVerboseModelsData = List[Union[VerboseModelCard, ProxyCard]]


class ListModelsResponse(BaseModel):
    object: str
    """The object type, which is always "list" for a list of model objects."""
    data: ListModelsData
    """The list of model/proxy cards."""
    count: int
    """The number of model/proxy cards returned."""


class ListVerboseModelsResponse(BaseModel):
    object: str
    """The object type, which is always "list" for a list of model objects."""
    data: ListVerboseModelsData
    """The list of model/proxy cards."""
    count: int
    """The number of model/proxy cards returned."""
