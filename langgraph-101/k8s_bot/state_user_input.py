from typing_extensions import TypedDict


class UserInputState(TypedDict):
    question: str
    is_valid: bool
    verifier_response: str
