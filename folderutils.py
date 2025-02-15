import ctypes
from pathlib import Path

# Library metadata
__lib_name__ = "FolderUtils"
__lib_version__ = "0.1.0-alpha"

# Print library info when imported
print(f"{__lib_name__} version {__lib_version__}")

# Mapping of common CSIDL constants to folder names
CSIDL_FOLDERS = {
    "DESKTOP": 0,              # Desktop
    "DOCUMENTS": 5,            # My Documents
    "MUSIC": 13,               # My Music
    "PICTURES": 39,            # My Pictures
    "VIDEOS": 14,              # My Videos
    "APPDATA": 26,             # Application Data (Roaming)
    "LOCAL_APPDATA": 28,       # Local Application Data
    "STARTMENU": 11,           # Start Menu
}


def get_folder(folder_name):
    """
    Retrieves the path to a specified special folder.

    Args:
        folder_name (str): Name of the folder (e.g., "DOCUMENTS", "DESKTOP").

    Returns:
        pathlib.Path: Path object pointing to the folder.

    Raises:
        ValueError: If the folder name is not recognized.
        OSError: If the folder path cannot be retrieved.
    """
    if folder_name not in CSIDL_FOLDERS:
        raise ValueError(f"Unknown folder name: {folder_name}")

    CSIDL = CSIDL_FOLDERS[folder_name]
    buffer = ctypes.create_unicode_buffer(260)  # MAX_PATH is 260 characters

    # SHGetFolderPathW to get the folder path
    result = ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL,
                                                    None, 0, buffer)
    if result != 0:
        raise OSError(f"Failed to retrieve the path for folder: {folder_name}")

    return Path(buffer.value)


# Example functions for specific folders
def get_desktop_folder():
    return get_folder("DESKTOP")


def get_documents_folder():
    return get_folder("DOCUMENTS")


def get_pictures_folder():
    return get_folder("PICTURES")


def get_music_folder():
    return get_folder("MUSIC")


def get_videos_folder():
    return get_folder("VIDEOS")


def get_appdata_folder():
    return get_folder("APPDATA")


def get_local_appdata_folder():
    return get_folder("LOCAL_APPDATA")
