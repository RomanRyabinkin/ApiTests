import pytest
from BaseDirectory.BaseModule import main_headers, test_headers
from Section.SectionRequests import Section


@pytest.mark.section_list
def test_section_list():
    section = Section()
    section.get_sections(headers=test_headers)


@pytest.mark.section_settings
def test_section_settings():
    section = Section()
    section.section_settings(headers=main_headers)


@pytest.mark.add_section
def test_add_section():
    section = Section()
    section.add_section()


@pytest.mark.get_section
def test_get_section():
    section = Section()
    section.get_section()


def test_edit_section():
    section = Section()
    section.edit_section()


def test_make_section_on_chat():
    section = Section()
    section.make_section_on_chat()


def test_delete_section_on_chat():
    section = Section()
    section.delete_section_on_chat()


def test_throw_off_section_settings():
    section = Section()
    section.throw_off_section_request()




if __name__ == '__main__':
    pytest.run()
