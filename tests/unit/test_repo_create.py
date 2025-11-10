def test_repo_create( empty_repo ):
    repo, repo_path = empty_repo
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
