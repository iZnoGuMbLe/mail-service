from pydantic import BaseModel


class UserMessageBody(BaseModel):
    type: str
    email: str
    username: str
    token: str