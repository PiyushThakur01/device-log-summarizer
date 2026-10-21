from clean_readings import clean_readings


def test_mixed_input():
    assert clean_readings(["12.5", None, -1, "abc", 700, "300", 0]) == [12.5, 500.0, 300.0, 0.0]


def test_empty_and_none():
    assert clean_readings([]) == []
    assert clean_readings(None) == []


def test_all_invalid():
    assert clean_readings([None, "x", -5, "-0.1", float("nan")]) == []


if __name__ == "__main__":
    test_mixed_input(); test_empty_and_none(); test_all_invalid()
    print("All tests passed")
