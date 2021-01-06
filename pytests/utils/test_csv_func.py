import os

from bot_top_ranking import work_with_csv
import pytest
import csv


@pytest.mark.smoke
def test_get_music_csv(set_temp_folder):
    test_song = {
        "title": "I'm the best tester",
        "author": "Mr.Fish",
        "link": "your link could be here",
    }
    expected_result = {
        "title": "I'm the best tester",
        "author": "Mr.Fish",
        "link": "your link could be here",
        "mark": 0,
        "pos": 1,
        "voted_users": []
    }
    file_name = "/".join(str(set_temp_folder).split("/")[:-1]) + "/test.csv"
    with open(file_name, mode="w", encoding='utf-8') as w_file:
        headers = ["title", "author", "link"]
        csv_writer = csv.DictWriter(w_file, delimiter=',', lineterminator='\r', fieldnames=headers)
        csv_writer.writeheader()
        csv_writer.writerow(test_song)
    returned_value = work_with_csv.get_music_csv(file_name)
    assert len(returned_value) == 1 and returned_value[0] == expected_result


@pytest.mark.smoke
def test_create_csv(set_temp_folder):
    file_name = "/".join(str(set_temp_folder).split("/")[:-1]) + "/test.csv"
    amount = 1
    work_with_csv.create_csv(file_name, amount)
    assert os.path.exists(file_name)
    os.remove(file_name)
