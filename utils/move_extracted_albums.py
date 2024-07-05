import os
import shutil


def find_and_move_extracted_files(source_dir, destination_dir):
    # Ensure the destination directory exists
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        # pass

    # Walk through the source directory
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.extracted'):
                # Get the full path of the file
                file_path = os.path.join(root, file)

                # Get the folder name
                folder_name = os.path.basename(root)

                # Create the new file name
                new_file_name = f"{os.path.splitext(file)[0]}_{folder_name}{os.path.splitext(file)[1]}"

                # Move and rename the file to the destination directory
                shutil.move(file_path, os.path.join(destination_dir, new_file_name))
                print(f"newfile ---  {os.path.join(destination_dir, new_file_name)}")
                #exit()


source_directory = '/volume1/flac_lib'
destination_directory = '/volume1/flac_full_albums'

find_and_move_extracted_files(source_directory, destination_directory)

