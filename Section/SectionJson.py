from BaseDirectory.BaseModule import api_version

def sorting_settings_function(sort, show):
    sections_settings_json = {
        "sort": sort,
        "show": show,
        "version": api_version
    }
    return sections_settings_json

def add_section_function(title, position, sort, show):
    add_section_json = {
        "title": title,
        "position": position,
        "sort": sort,
        "show": show,
        "version": api_version
    }
    return add_section_json


def edit_section_function(hash, title, position, sort, show):
    json_for_edit_section = {
        "hash": hash,
        "title": title,
        "position": position,
        "sort": sort,
        "show": show,
        "version": api_version
    }
    return json_for_edit_section

def json_for_throw_section(sort_default, show_default):
    json = {
        "sort_default": sort_default,
        "show_default": show_default,
        "version": api_version
    }
    return json
