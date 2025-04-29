import configparser

from repo_review.testing import compute_check


def test_scfg001():
    setupcfg = configparser.ConfigParser()
    setupcfg.read_string("""
        [metadata]
        name = foo
        version = 1.0
        description = A test package
        author = Me
        author_email = me@example.com
        """)
    assert compute_check("SCFG001", setupcfg=setupcfg).result


def test_scfg001_invalid():
    setupcfg = configparser.ConfigParser()
    setupcfg.read_string("""
        [metadata]
        name = foo
        version = 1.0
        description = A test package
        author = Me
        author-email = me@example.com
        """)
    answer = compute_check("SCFG001", setupcfg=setupcfg)
    assert not answer.result
    assert "metadata.author-email" in answer.err_msg


def test_no_setupcfg():
    assert compute_check("SCFG001", setupcfg=None).result is None
