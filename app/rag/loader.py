from typing import Union

def load_text_file(file) -> str:
    """
    Reads uploaded text file and returns content as string.
    """
    data: Union[bytes, str] = file.read()

    # If it's already a string, return it
    if isinstance(data, str):
        return data

    # If it's bytes, decode to string
    return data.decode("utf-8", errors="replace")
