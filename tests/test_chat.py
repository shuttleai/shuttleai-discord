from shuttleai.schemas.chat.completions import (
    ChatCompletionResponse,
    ChatCompletionStreamResponse,
    ChatMessage,
)


class TestChat:
    def test_chat(self, client):
        result = client.chat.completions.create(
            model="shuttle-2-turbo",
            messages=[ChatMessage(role="user", content="What is 2 plus 3?")],
        )

        assert isinstance(result, ChatCompletionResponse), "Should return an ChatCompletionResponse"
        assert len(result.choices) == 1
        assert result.choices[0].index == 0
        assert result.object == "chat.completion"

    def test_chat_streaming(self, client):
        result = client.chat.completions.create(
            model="shuttle-2-turbo",
            messages=[ChatMessage(role="user", content="What is 2 plus 3?")],
            stream=True
        )

        results = list(result)

        for i, result in enumerate(results):
            if i == 0:
                assert isinstance(result, ChatCompletionStreamResponse), "Should return an ChatCompletionStreamResponse"
                assert len(result.choices) == 1
                assert result.choices[0].index == 0
                assert result.choices[0].delta.role == "assistant"
            else:
                assert isinstance(result, ChatCompletionStreamResponse), "Should return an ChatCompletionStreamResponse"
                assert len(result.choices) == 1
                assert result.choices[0].index == i - 1
                assert result.choices[0].delta.content == f"stream response {i-1}"
                assert result.object == "chat.completion.chunk"
