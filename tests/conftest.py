import pytest
from histree.Repo import repo_create

@pytest.fixture
def empty_repo( tmp_path ):
    """
    Creates an empty repo in a temporary directory and returns its path + object.
    Automatically cleaned up by pytest.
    """
    repo_path = tmp_path / "repo"
    repo = repo_create( str( repo_path ) )
    return repo, repo_path
