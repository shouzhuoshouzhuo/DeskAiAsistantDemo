from core.prompt_builder import build_messages, get_system_message
from core.ai_client import AIClient
from core.memory import load_profile, update_after_chat

_client = AIClient()

def route(mode: str, user_input: str, history: list[dict] = None) -> str:
    if mode == "Chat":
        system_msg = get_system_message()
        messages = [system_msg] + (history or []) + [{"role": "user", "content": user_input}]
    else:
        messages = build_messages(mode, user_input)
    result = _client.chat(messages)
    if mode == "Chat":
        profile = load_profile()
        update_after_chat(profile, user_input)
    return result