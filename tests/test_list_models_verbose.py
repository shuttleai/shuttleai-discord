#  type: ignore
from shuttleai.schemas.models.models import ListVerboseModelsResponse


class TestListModels:
    def test_list_models(self, client):

        result = client.list_models_verbose()

        assert isinstance(result, ListVerboseModelsResponse), "Should return an ListVerboseModelsResponse"
        assert len(result.data) == 142
        assert result.object == "list"
        assert result.count == 142
