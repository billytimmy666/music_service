import os
import shutil


def find_and_move_mp3_folders(source_dir, destination_dir):
    # Ensure the destination directory exists
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Dictionary to track folders containing mp3 files
    folders_to_move = {}

    # Walk through the source directory
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.mp3'):
                # If an mp3 file is found, mark the folder for moving
                relative_folder = os.path.relpath(root, source_dir)
                folders_to_move[root] = relative_folder

    # Move folders to the destination, retaining structure
    for folder, relative_folder in folders_to_move.items():
        destination_folder = os.path.join(destination_dir, relative_folder)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        for item in os.listdir(folder):
            if "@eaDir" in item:
                continue
            source_item = os.path.join(folder, item)
            destination_item = os.path.join(destination_folder, item)
            if os.path.isdir(source_item):
                shutil.copytree(source_item, destination_item)
                print(f"copy {source_item} --- {destination_item}")
            else:
                print(f"move {source_item} +++++ {destination_item}")
                shutil.move(source_item, destination_item)

        if folder == source_dir:
            exit()
        # Remove the empty source folder
        shutil.rmtree(folder)
        print(f"Moved folder: {folder} to {destination_folder}")
        #exit()


# Example usage
source_directory = '/volume1/flac_lib'
destination_directory = '/volume1/mp3-temp'

find_and_move_mp3_folders(source_directory, destination_directory)

