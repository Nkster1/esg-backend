# Models
from typing import List, Tuple, Dict

from pydantic import BaseModel


class CompanyDescription(BaseModel):
    description: str
    # todo potentially add more information like segment etc.


class ChatMessage(BaseModel):
    message: str
    sender: str


class ChatRequest(BaseModel):
    new_message: ChatMessage
    previous_messages: List[ChatMessage]

    def to_conversation_buffer_memory_format(self) -> List[Tuple[Dict[str, str]]]:
        """
        transform frontend data into necessary format for langchain memory buffer
        """
        output = []
        # previous_messages always alternating inputs from user and responses from ai model, first message always
        # from user
        user_messages = []
        ai_messages = []
        for message in self.previous_messages:
            if message.sender == "user":
                user_messages.append({"input": message.message})
            elif message.sender == "ai":
                ai_messages.append({"output": message.message})
            else:
                raise ValueError(
                    f"message.sender: {message.sender} not valid, has to be either 'ai' or 'user'"
                )

        return list(zip(user_messages, ai_messages))
