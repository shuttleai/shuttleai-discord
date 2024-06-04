from pydantic import BaseModel, Field


class ModerationCategoryScores(BaseModel):
    sexual: float = Field(alias="sexual")
    hate: float = Field(alias="hate")
    harassment: float = Field(alias="harassment")
    self_harm: float = Field(alias="self-harm")
    sexual_minors: float = Field(alias="sexual/minors")
    hate_threatening: float = Field(alias="hate/threatening")
    violence_graphic: float = Field(alias="violence/graphic")
    self_harm_intent: float = Field(alias="self-harm/intent")
    self_harm_instructions: float = Field(alias="self-harm/instructions")
    harassment_threatening: float = Field(alias="harassment/threatening")
    violence: float = Field(alias="violence")


class ModerationResult(BaseModel):
    flagged: bool
    categories: ModerationCategoryScores
    category_scores: ModerationCategoryScores


class ModerationResponse(BaseModel):
    id: str
    model: str
    results: list[ModerationResult]
