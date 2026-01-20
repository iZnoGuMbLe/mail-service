from pydantic import BaseModel


class UserMessageBody(BaseModel):
    user_email: str
    subject: str
    message: str