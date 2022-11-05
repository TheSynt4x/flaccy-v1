WHITELIST = [
    (":", ""),
    ("\\", ""),
    ("<", ""),
    (">", ""),
    ("?", ""),
    ("|", ""),
    ("*", ""),
    ("/", ""),
    ('"', ""),
    ("‐", "-"),
]


def clean_filename(str):
    for k, v in WHITELIST:
        str = str.replace(k, v)

    return str
