from pydantic import BaseModel, Field


class ConvertCurrecnyQuery(BaseModel):
    from_: str = Field(
        ...,
        min_length=3,
        max_length=3,
        to_upper=True,
        alias="from",
        description="Currency to convert from",
    )
    to: str = Field(
        ...,
        min_length=3,
        max_length=3,
        to_upper=True,
        description="Currency to convert to",
    )
    amount: float = Field(..., gt=0, description="Amount of currency to convert")


class UpdateRatesQuery(BaseModel):
    merge: int = Field(..., ge=0, le=1, description="0: flush, 1: update ")


class UpdateCurrencyRate(BaseModel):
    currency_pair: str = Field(..., regex="^[a-zA-z]{3}\/[a-zA-z]{3}", to_upper=True)
    rate: float


class UpdateRatesBody(BaseModel):
    pairs: list[UpdateCurrencyRate]
