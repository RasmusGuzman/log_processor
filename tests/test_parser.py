from log_processor.models import LogEntry
from log_processor.parser import LogParser


def test_log_parser(temp_log_file):
    parser = LogParser([temp_log_file])
    entries = parser.parse()

    assert len(entries) == 2
    assert isinstance(entries[0], LogEntry)
    assert entries[0].url == "/api/context/1"
    assert entries[1].url == "/api/context/2"


def test_invalid_log_file(tmpdir):
    invalid_file = tmpdir.join("invalid.log")
    with open(invalid_file, "w") as f:
        f.write("This is not JSON\n")

    parser = LogParser([str(invalid_file)])
    entries = parser.parse()

    assert len(entries) == 0


def test_empty_log_file(tmpdir):
    empty_file = tmpdir.join("empty.log")
    with open(empty_file, "w"):
        pass  # пустой файл

    parser = LogParser([str(empty_file)])
    entries = parser.parse()

    assert len(entries) == 0
