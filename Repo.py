import configparser
import os

''' UTILITY FUNCTIONS '''
def repo_path( repo, *path ):
    return os.path.join( repo.gitdir, *path )

def repo_dir( repo, *path, mkdir=False ):
    path = repo_path( repo, *path )

    if os.path.exists( path ):
        if ( os.path.isdir( path ) ):
            return path
        else:
            raise Exception( f"Not a directory {path}" )

    if mkdir:
        os.makedirs( path )
        return path
    else:
        return None

def repo_file( repo, *path, mkdir=False ):
    if repo_dir( repo, *path[:-1], mkdir=mkdir ):
        return repo_path( repo, *path )

''' REPO CLASS '''
class GitRepository( object ):
    """ a git repository """
    '''
        a git repository has:
            1. Work Tree - this contains the files to be tracked
            2. Git Directory - this is within the working directory (.git) and
            contains metadata of the repository
    '''

    worktree = None
    gitdir = None
    conf = None

    def __init__( self, path, force=False ):
        self.worktree = path
        self.gitdir = os.path.join( path, ".git" )

        if not ( force or os.path.isdir( self.gitdir ) ):
            raise Exception( f"Not a Git repository: {path}" )

        # .git/config
        self.conf = configparser.ConfigParser()
        cf = repo_file( self, "config" )

        if cf and os.path.exists( cf ):
            self.conf.read( [ cf ] )
        elif not force:
            raise Exception( f"Configuration file missing" )

        if not force:
            version = int( self.conf.get( "core", "repositoryformatversion" ) )
            if version != 0:
                raise Exception( "Unsupported repositoryformatversion: " \
                        "{version}" )

def repo_default_config():
    ret = configparser.ConfigParser()

    ret.add_section( "core" )
    ret.set( "core", "repositoryformatversion", "0" )
    ret.set( "core", "filemode", "false" )
    ret.set( "core", "bare", "false" )
    # git also supports a optional 'worktree' key
    # our simple version control doesn't support it

    return ret

def repo_create( path ):
    repo = GitRepository( path, True )

    if os.path.exists( repo.worktree ):
        if not os.path.isdir( repo.worktree ):
            raise Excpetion( f"{path} is not a directory!" )
        if os.path.exists( repo.gitdir ) and os.listdir( repo.gitdir ):
            raise Exception( f"{path} is not empty!" )
    else:
        os.makedirs( repo.worktree )

    assert repo_dir( repo, "branches", mkdir=True )
    assert repo_dir( repo, "objects", mkdir=True )
    assert repo_dir( repo, "refs", "tags", mkdir=True )
    assert repo_dir( repo, "refs", "heads", mkdir=True )

    # .git/description
    with open( repo_file( repo, "description" ), "w" ) as f:
        f.write( "Unnamed repository; edit this file 'description' to name " \
                "the repository.\n" )

    # .git/HEAD
    with open( repo_file( repo, "HEAD" ), "w" ) as f:
        f.write( "ref: refs/heads/master\n" )

    with open( repo_file( repo, "config" ), "w" ) as f:
        config = repo_default_config()
        config.write( f )

    return repo
