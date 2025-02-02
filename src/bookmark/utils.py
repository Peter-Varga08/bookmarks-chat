from collections import defaultdict


def get_valid_folders_dict() -> defaultdict[str, bool]:
    valid_folders = ["cs", "wacc", "cloud", "ai practical"]
    initial_dict = {folder: True for folder in valid_folders}
    return defaultdict(bool, initial_dict)
