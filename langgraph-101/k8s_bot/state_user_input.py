from k8s_bot.state_main import MainState


class UserInputState(MainState):
    question: str
    is_valid: bool
    verifier_response: str
