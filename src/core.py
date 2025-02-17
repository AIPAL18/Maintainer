import re
import urllib.request
from zipfile import ZipFile
import os
import shutil


def parse_version(version: str):
    VERSION_PATTERN = r"""
        ^(?P<major>0|[1-9]\d*)
        \.
        (?P<minor>0|[1-9]\d*)
        \.
        (?P<patch>0|[1-9]\d*)
        (?:-
            (?P<prerelease>
                (?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)
                (?:\.
                    (?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)
                )*
            )
        )?
        (?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?
        $
    """
    _regex = re.compile(r"^\s*" + VERSION_PATTERN + r"\s*$", re.VERBOSE | re.IGNORECASE)

    # Validate the version and parse it into pieces
    match = _regex.search(version)
    if not match:
        print("error")
        return
    
    major = int(match.group("major"))
    minor = int(match.group("minor"))
    patch = int(match.group("patch"))
    prerelease = match.group("prerelease")
    prerelease_number = 0
    if prerelease:
        prerelease_number = float("inf")
        prerelease = prerelease.split(".")
        match prerelease[0]:
            case "poc":
                prerelease_number = 100
            case "alpha":
                prerelease_number = 200
            case "beta":
                prerelease_number = 300

        if len(prerelease) > 1:
            prerelease_number += int(prerelease[1])

    return (major, minor, patch, prerelease_number)


def get_greater_version(releases):
    max_release = None
    max_version = parse_version("0.0.0")
    is_pre = True
    for release in releases:
        # tag_name
        # created_at
        # prerelease
        tag =  release["tag_name"]
        str_version = tag[1:]
        version = parse_version(str_version)
        prerelease = release["prerelease"]

        # True > False
        if version > max_version and (is_pre <= prerelease):
            max_release = release
            max_version = version
            is_pre = prerelease
        elif is_pre and not prerelease:
            max_release = release
            max_version = version
            is_pre = prerelease

    return max_release


def download(link: str, filename: str):
    return urllib.request.urlretrieve(link, filename)


def unzip(path: str, destination: str):
    filename = ""
    # loading the temp.zip and creating a zip object 
    with ZipFile(path, 'r') as zObject: 
    
        # Extracting all the members of the zip  
        # into a specific location. 
        zObject.extractall(path=destination)
        filename = zObject.filelist[0].filename[:-1]
        zObject.close()

    return filename


def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        print("file {} is not a file or dir.".format(path))


def rename(path: str, name: str):
    new = os.path.join(os.path.dirname(path), name)
    print(path, new)
    os.rename(path, new)
