import subprocess

def test_init( tmp_path ):
    repo_path = tmp_path / "testrepo"

    result = subprocess.run(
        [ "python3", "src/histree/histree", "init", str( repo_path ) ],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"init command failed: {result.stderr}"

    git_dir = repo_path / ".git"
    assert git_dir.is_dir(), f"Missing directory: {git_dir}"

    expected_dirs = [
        "branches",
        "objects",
        "refs",
        "refs/heads",
        "refs/tags",
    ]
    for dir in expected_dirs:
        assert ( git_dir / dir ).is_dir(), f"Missing directory: {git_dir/dir}"

    desc_file = git_dir / "description"
    head_file = git_dir / "HEAD"
    config_file = git_dir / "config"
    assert desc_file.is_file(), "Missing description file"
    assert head_file.is_file(), "Missing HEAD file"
    assert config_file.is_file(), "Missing config file"

    assert "Unnamed repository" in desc_file.read_text()
    assert "ref: refs/heads/master" in head_file.read_text()
    config_text = config_file.read_text()
    assert "repositoryformatversion = 0" in config_text
    assert "filemode = false" in config_text
    assert "bare = false" in config_text
