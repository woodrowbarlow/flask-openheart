"""Generate a JSON file containing information about every emoji."""

import argparse
import json
import urllib.request

DEFAULT_UNICODE_VERSION = "16.0"


def data(unicode_version):
    """Open the Unicode Emoji test data file for a given unicode version and yield each line."""
    url = f"https://unicode.org/Public/emoji/{unicode_version}/emoji-test.txt"
    with urllib.request.urlopen(url) as f:  # noqa: S310
        for line in f:
            yield line.decode("utf-8")


def parse(line):
    """Parse a line of data about a specific emoji."""
    [codepoints_str, line] = line.strip().split(";", maxsplit=1)
    [status, line] = line.strip().split("#", maxsplit=1)
    [emoji, version, description] = line.strip().split(None, maxsplit=2)
    codepoints = [chr(int(code, 16)) for code in codepoints_str.strip().split()]
    assert emoji == "".join(codepoints)  # noqa: S101
    return emoji, {
        "status": status.strip(),
        "version": version.strip(),
        "description": description.strip(),
    }


def emojis(unicode_version):
    """Iterate through each emoji in the unicode test data file, yield the emoji and a details struct."""
    group = None
    subgroup = None
    count = 0
    for line in data(unicode_version):
        if not line.strip():
            continue
        if not line.startswith("#"):
            emoji, details = parse(line)
            details.update({"group": group, "subgroup": subgroup})
            yield emoji, details
            count += 1
        elif line.startswith("# group:"):
            count = 0
            group = line.split(":", maxsplit=1)[1]
            group = group.strip()
        elif line.startswith("# subgroup:"):
            subgroup = line.split(":", maxsplit=1)[1]
            subgroup = subgroup.strip()
        elif line.startswith(f"# {group} subtotal:"):
            if line.strip().endswith("w/o modifiers"):
                continue
            subtotal = int(line.split(":", maxsplit=1)[1].strip())
            assert subtotal == count  # noqa: S101


def generate(args):
    """Process all emojis and print them as JSON."""
    print(json.dumps(dict(emojis(args.unicode_ver)), indent=2))  # noqa: T201


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--unicode-ver", default=DEFAULT_UNICODE_VERSION)
    args = parser.parse_args()
    generate(args)
