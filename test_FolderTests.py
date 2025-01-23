import pytest

from Folder.FolderRequests import Folder


@pytest.mark.folders
def test_folders():
    folder = Folder()
    folder.create_folder_in_chat(subject_hash=folder.test_chat_hash,
                                 title=folder.generate_random_string(10), sort=510,
                                 headers=folder.get_headers(folder.main_user_token_url), status_code=200)
    # Запрос без авторизации
    folder.create_folder_in_chat(subject_hash=folder.test_chat_hash,
                                 title=folder.generate_random_string(10), sort=500,
                                 headers=None, status_code=401)
    # Запрос без title
    folder.create_folder_in_chat(subject_hash=folder.test_chat_hash,
                                 title=None, sort=500,
                                 headers=folder.get_headers(folder.main_user_token_url), empty_title=True)
    # Запрос без subject_hash
    folder.create_folder_in_chat(subject_hash=None,
                                 title=folder.generate_random_string(), sort=500,
                                 headers=folder.get_headers(folder.main_user_token_url), empty_subject_hash=True)
    # Запрос без параметра sort
    folder.create_folder_in_chat(subject_hash=folder.test_chat_hash,
                                 title=folder.generate_random_string(),
                                 sort = None, headers=folder.get_headers(folder.main_user_token_url),
                                 empty_sort_param=True)
    # Запрос на сортировку уже существующей папки в чате.
    folder.folder_sort(status_code=200, headers=folder.get_headers(folder.main_user_token_url))
    # Запрос на сортировку папки в чате без авторизации
    folder.folder_sort(status_code=401, headers=None)
    # Запрос на сортировку папки в чате без хэша папки
    folder.folder_sort(empty_folder_hash=True, headers=folder.get_headers(folder.main_user_token_url))
    # Запрос на сортировку папки в чате без сортировочного параметра
    folder.folder_sort(empty_sort_param=True, headers=folder.get_headers(folder.main_user_token_url))
    # Запрос на изменение названия уже существующей папки в чате
    folder.rename_folder(status_code=200, headers=folder.get_headers(folder.main_user_token_url), hash_chat=folder.test_chat_hash)
    # Запрос на изменение названия папки в чате без авторизации
    folder.rename_folder(status_code=401, headers=folder.get_headers(folder.main_user_token_url))
    # Запрос на изменение названия папки с некорректным хэшем папки
    folder.rename_folder(empty_folder_hash=True, headers=folder.get_headers(folder.main_user_token_url))
    # Запрос на изменение названия папки без указания нового title папки
    folder.rename_folder(empty_folder_title=True, headers=folder.get_headers(folder.main_user_token_url))
    # Запрос на удаление папки из чата
    folder.delete_folder(folder_hash=None, headers=folder.get_headers(folder.main_user_token_url), status_code=200, hash_chat=folder.test_chat_hash)
    folder.delete_folder(folder_hash=None, headers=folder.get_headers(folder.main_user_token_url), status_code=200, hash_chat=folder.test_chat_hash)
    # Запрос на удаление папки из чата без авторизации
    folder.delete_folder(folder_hash="b12b92af-48b8-4e50-8c4a-57f08ae4a098", headers=None, status_code=401)
    # Запрос на удаление папки с несуществующим хэшем
    folder.delete_folder(folder_hash=None, headers=folder.get_headers(folder.main_user_token_url), non_existent_hash=True)



