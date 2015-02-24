
""" Utility functions. """

import re


def splitc(s, delimiter, strip=False, discard_empty=False, maxsplit=-1):
    """ Splits a string on instances of a delimiter character.

    Ignores quoted delimiters.

    """
    tokens, buf, expecting, escaped = [], [], None, False

    for index, char in enumerate(s):
        if expecting:
            buf.append(char)
            if char == expecting and not escaped:
                expecting = None
        else:
            if char == delimiter:
                tokens.append(''.join(buf))
                buf = []
                if len(tokens) == maxsplit:
                    buf.append(s[index+1:])
                    break
            else:
                buf.append(char)
                if char in ('"', "'"):
                    expecting = char
        escaped = not escaped if char == '\\' else False

    tokens.append(''.join(buf))

    if strip:
        tokens = [t.strip() for t in tokens]

    if discard_empty:
        tokens = [t for t in tokens if t]

    return tokens


def splitws(s, maxsplit=-1):
    """ Splits a string on blocks of whitespace.

    Strips leading and trailing whitespace. Ignores quoted whitespace.

    """
    tokens, buf, expecting, escaped, wsrun = [], [], None, False, False

    for index, char in enumerate(s.strip()):
        if expecting:
            buf.append(char)
            if char == expecting and not escaped:
                expecting = None
        else:
            if char.isspace():
                if wsrun:
                    continue
                tokens.append(''.join(buf))
                buf = []
                wsrun = True
                if len(tokens) == maxsplit:
                    buf.append(s[index+1:].lstrip())
                    break
            else:
                buf.append(char)
                wsrun = False
                if char in ('"', "'"):
                    expecting = char
        escaped = not escaped if char == '\\' else False

    tokens.append(''.join(buf))
    return tokens


def splitre(s, delimiters, keepdels=False):
    """ Splits a string using a list of regular expression patterns.

    Ignores quoted delimiter matches.

    """
    tokens, buf = [], []
    end_last_match = 0

    pattern = r'''"(?:[^\\"]|\\.)*"|'(?:[^\\']|\\.)*'|%s'''
    pattern %= '|'.join(delimiters)

    for match in re.finditer(pattern, s):
        if match.group()[0] in ["'", '"']:
            buf.append(s[end_last_match:match.end()])
            end_last_match = match.end()
            continue
        buf.append(s[end_last_match:match.start()])
        tokens.append(''.join(buf))
        buf = []
        end_last_match = match.end()
        if keepdels:
            tokens.append(match.group())

    buf.append(s[end_last_match:])
    tokens.append(''.join(buf))

    return tokens