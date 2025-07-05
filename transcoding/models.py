from typing import Dict, TypedDict


class TranscodingInformation(TypedDict):
    scaling: str
    options: Dict[str, str]
    two_pass: bool
    options_second_pass: Dict[str | None]
    