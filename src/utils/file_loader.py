import os


def get_input_options(directory):
    try:
        files = [
            f
            for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))
        ]

        files.sort()
        return files

    except FileNotFoundError:
        return []
