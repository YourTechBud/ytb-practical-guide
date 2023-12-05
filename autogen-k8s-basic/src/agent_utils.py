def is_termination_message(content):
    have_content = content.get("content", None) is not None
    if have_content and "Done" in content["content"]:
        return True
    return False
