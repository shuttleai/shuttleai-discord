from shuttleai.schemas.models.models import ListModelsResponse


class TestListModels:
    def test_list_models(self, client):

        result = client.list_models()

        assert isinstance(result, ListModelsResponse), "Should return an ListModelsResponse"
        assert len(result.data) == 142
        assert result.object == "list"
        assert result.count == 142
