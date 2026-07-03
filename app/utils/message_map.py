_message_map: dict[tuple[int, int], int] = {}


def add_mapping(chat_id: int, message_id: int, other_chat_id: int) -> None:
    _message_map[(chat_id, message_id)] = other_chat_id


def get_mapping(chat_id: int, message_id: int) -> int | None:
    return _message_map.get((chat_id, message_id))


def remove_mapping(chat_id: int, message_id: int) -> None:
    _message_map.pop((chat_id, message_id), None)
