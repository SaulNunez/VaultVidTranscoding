
import os


def get_resulting_filename(s3_object_name: str, transcoding_option: str) -> str:
    path, file_name = os.path.split(s3_object_name)

    result = os.path.join(path, transcoding_option.strip(), file_name)

    return result