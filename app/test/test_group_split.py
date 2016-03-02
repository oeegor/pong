# coding: utf-8

from utils import split_players_to_groups


def test_split_players():

    groups = split_players_to_groups(['a'] * 10)
    assert groups == [['a'] * 5] * 2

    groups = split_players_to_groups(['a'] * 6)
    assert groups == [['a'] * 6]

    groups = split_players_to_groups(['a'] * 16)
    assert groups == [['a'] * 4] * 4

    groups = split_players_to_groups(['a'] * 17)
    assert groups == [['a'] * 5] + [['a'] * 4] * 3
