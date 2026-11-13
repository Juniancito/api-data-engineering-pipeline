from pydantic import BaseModel, ConfigDict, EmailStr, Field

class AddressSchema(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    city: str | None = None 

class CompanySchema(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    name: str | None = None

class UserSchema(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: int = Field(gt=0)
    name: str | None = Field(default=None, min_length=1)
    username: str | None = Field(default=None, min_length=1)
    email: EmailStr

    address: AddressSchema | None = None
    company: CompanySchema | None = None