from fastapi import Form
from pydantic import BaseModel, validator

from app.auth.crud import get_user_by_email

import inspect
from typing import Type

from fastapi import Form
from pydantic import BaseModel

# helper function (for forms)
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

# data schemas
@as_form
class LoginSchema(BaseModel):
    email: str = Form(alias='email')
    password: str = Form(alias='password')

@as_form
class RegisterSchema(BaseModel):
    email: str = Form(alias='email')
    password: str = Form(alias='password')