"""One Line, One Laugh — writes a single one-line joke to entry.txt."""

import os
import stat
import tempfile

ENTRY = "My mechanic said my brakes were fine, my tires were fine, my engine was fine \u2014 then charged me $400 to tell me everything was fine."


def validate(text):
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be empty or whitespace-only")
    if len(text) > 200:
        raise ValueError(f"entry is {len(text)} characters, over the 200-character limit")
    if len(text) < 1:
        raise ValueError("entry must be at least 1 character")
    if "\n" in text:
        raise ValueError("entry must be a single line (contains a newline)")
    if "\r" in text:
        raise ValueError("entry must be a single line (contains a carriage return)")
    text.encode("utf-8")
    return text


def main():
    entry = validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    data = entry.encode("utf-8")
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, target)
        os.chmod(target, 0o644)
        # Read-back verification: the written file must be byte-identical.
        with open(target, "rb") as f:
            written = f.read()
        if written != data:
            raise IOError("read-back verification failed: entry.txt bytes differ from entry")
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
