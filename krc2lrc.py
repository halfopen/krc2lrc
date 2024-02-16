import zlib
import re


def krc_decode(content):
    # (bytes)->str
    """

    :param content:
    :return:
    """
    encrypt_key = (64, 71, 97, 119, 94, 50, 116, 71, 81, 54, 49, 45, 206, 210, 110, 105)
    content = content[4:]
    compress_content = bytes(content[i] ^ encrypt_key[i % len(encrypt_key)] for i in range(len(content)))
    text_bytes = zlib.decompress(bytes(compress_content))
    text = text_bytes.decode("utf8")
    return text


def krc2lrc(text):
    """
        decode krc format into lrc format
        sample input: [108,90]<0,0,0>作<0,17,0>词：<17,0,0>黄<17,47,0>俊<64,26,0>郎
        sample output: [00:00.10]作词：黄俊郎
    """
    output = []
    for line in text.split("\n"):
        output.append(parse_line(line))
    return "\n\n".join(output)


def parse_line(line):
    ts_re = r"^\[(\d+),(\d+)\]"
    ts_re2 = r"<\d+,\d+,\d+>"
    m = re.match(ts_re, line)
    if m:
        ts = ts2str(int(m.group(1)))
        lyrics = re.sub(ts_re, "", line)
        lyrics = re.sub(ts_re2, "", lyrics)
        return f"[{ts}]{lyrics}"
    return line


def ts2str(ts):
    """

    :param ts:
    :return:
    """
    minutes = "%02d" % int(ts/1000/60)
    seconds = "%.2f" % ((ts - int(minutes)*60*1000)/1000)
    return f"{minutes}:{seconds}"


if __name__ == "__main__":

    with open("data/input.krc", "rb") as f:
        krc_content = f.read()

    krc_decode_content = krc_decode(krc_content)
    with open("data/krc_decode.txt", "w", encoding="utf-8") as f:
        f.write(krc_decode_content)

    lrc_content = krc2lrc(krc_decode_content)

    with open("data/output.lrc", "w") as f:
        f.write(lrc_content)