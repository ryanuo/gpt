def handle_ai_response(completion_content) -> str:
    if completion_content.find("chatkf123") != -1:
        completion_content = 'sorry, please retry later....'
    elif completion_content.find("Upgrade for higher rate limits") != -1:
        completion_content = 'sorry, please retry later....'
    return completion_content