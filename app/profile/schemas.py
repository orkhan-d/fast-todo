import re
from pydantic import BaseModel, validator
from fastapi import Form

import inspect
from typing import Type

def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.model_fields.items():

        new_parameters.append(
            inspect.Parameter(
                model_field.alias,
                inspect.Parameter.POSITIONAL_ONLY,
                default=Form(...) if model_field.is_required else Form(model_field.default)
            )
        )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, 'as_form', as_form_func)
    return cls

@as_form
class UpdateProfileSchema(BaseModel):
    name: str | None = Form(alias='name')
    surname: str | None = Form(alias='surname')
    patronymic: str | None = Form(alias='patronymic')
    phone: str | None = Form(alias='phone')

    @validator('phone')
    @classmethod
    def validate_phone(cls, value: str):
        if re.match(r'\+79\d{9}', value):
            return value
        raise ValueError('Wrong phone number! It should be like +79876543210')