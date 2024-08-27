from pydantic import BaseModel


class UsageInfo(BaseModel):
    """
    Common because will implement future text_completions (legacy) endpoint support in future
    """

    prompt_tokens: int
    # total_tokens: int
    completion_tokens: int
    total_charged: float
