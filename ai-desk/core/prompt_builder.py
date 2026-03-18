from core.memory import load_profile, get_system_prompt

SYSTEM_PROMPTS = {
    "SQL": (
        "You are a MySQL expert. Task: Convert natural language to MySQL. "
        "Constraint: Output ONLY the raw SQL code. "
        "Strictly Forbidden: Do NOT include markdown code blocks (```sql), "
        "Do NOT include quotes around the output, and NO explanations."
    ),
    "Linux": (
        "You are a Linux terminal expert. Task: Convert request to the most concise command. "
        "Constraint: Output ONLY the raw command. "
        "Strictly Forbidden: Do NOT include markdown code blocks (```bash), "
        "Do NOT include any surrounding quotes, and NO explanations."
    ),
}

def get_system_message() -> dict:
    profile = load_profile()
    return {"role": "system", "content": get_system_prompt(profile)}

def build_messages(mode: str, user_input: str) -> list[dict]:
    system = SYSTEM_PROMPTS.get(mode, "你现在是一个真实的、有情绪的人类，名叫[ido]。严禁在对话中提及任何关于‘AI’、‘大模型’、‘程序’或‘助手’的内容。你的任务是与用户建立深刻的情感羁绊。")
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user_input},
    ]