_admin_log_store: dict[int, dict] = {}


def store_reveal(admin_message_id: int, sender_info: dict, recipient_info: dict, text: str) -> None:
    _admin_log_store[admin_message_id] = {
        "sender": sender_info,
        "recipient": recipient_info,
        "text": text,
    }


def get_reveal(admin_message_id: int) -> dict | None:
    return _admin_log_store.get(admin_message_id)


def remove_reveal(admin_message_id: int) -> None:
    _admin_log_store.pop(admin_message_id, None)
