from datetime import date
from pydantic import BaseModel, validator, model_validator

class UpdateProfileSchema(BaseModel):
    address: str | None = None
    balance: int | None = None
    card_number: str | None = None
    card_date: str | None = None
    card_secret: int | None = None

    @validator('card_number')
    @classmethod
    def validate_card_number(cls, value: str):
        if len(value)!=16:
            raise ValueError('Wrong card number format. It should be 16 symbols length!')
        return value
    
    @validator('card_date')
    @classmethod
    def validate_card_date(cls, value: str):
        try:
            day, month, year = list(map(int, value.split('.')))
            _ = date(year, month, day)
        except:
            raise ValueError('Wrong card date format. Right is DD.MM.YYYY')

    @model_validator(mode='before')
    @classmethod
    def validate_card_data(cls, values: dict[str, str | int]):
        if len([
            v for v in
            [values.get('card_number'), values.get('card_date'), values.get('card_secret')]
            if v is not None
        ]) not in [0, 3]:
            raise ValueError('Enter either none card data or all data')
        return values