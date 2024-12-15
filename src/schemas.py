from pydantic import BaseModel, EmailStr, constr, validator
import re

class Session(BaseModel):
    id: int
    token: str

class Course(BaseModel):
    id: int
    name: str
    start: str
    end: str
    location: str
    hill: str
    img: str

class Registration(BaseModel):
    id: int
    session_id: int
    course_id: int
    name: constr(min_length=0, max_length=50)
    email: EmailStr
    phone: constr(min_length=9, max_length=9)
    children_count: int
    adults_count: int
    created_at: str

    @validator('name')
    def validate_full_name(cls, v):
        if not re.match(r'^[A-Za-zÁáČčĎďÉěÍíŇňÓóŘřŠšŤťÚúÝýŽž]+$', v):
            raise ValueError('Full name must contain only letters and spaces')
        return v

    @validator('phone')
    def validate_phone(cls, v):
        if not re.match(r'\d$', v):
            raise ValueError('Phone number must be between 9 and 15 digits and can include country code')
        return v