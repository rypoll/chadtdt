import os

def get_data_files(start_path):
    data_files = []
    for foldername, _, filenames in os.walk(start_path):
        for filename in filenames:
            data_files.append((os.path.join(foldername, filename), os.path.join(foldername.replace(start_path, '', 1), filename)))
    return data_files

start_path = '01-processing-files'
data_files = get_data_files(start_path)
print(data_files)
