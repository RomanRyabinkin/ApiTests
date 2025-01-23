from BaseDirectory.BaseModule import api_version


def get_activity(type, unread, offset, limit):
    json_for_get_activity = {
        "type": type,
        "unread": unread,
        "offset": offset,
        "limit": limit,
        "version": api_version

    }
    return json_for_get_activity