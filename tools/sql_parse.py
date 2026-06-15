"""sitecontents.sql / mcolumn.sql 의 INSERT VALUES 행을 파싱하는 유틸리티."""
import re


def unescape_mysql_string(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            nxt = s[i + 1]
            mapping = {
                '0': '\0', "'": "'", '"': '"', 'b': '\b',
                'n': '\n', 'r': '\r', 't': '\t', 'Z': '\x1a',
                '\\': '\\', '%': '%', '_': '_',
            }
            if nxt in mapping:
                out.append(mapping[nxt])
                i += 2
                continue
            else:
                out.append(nxt)
                i += 2
                continue
        out.append(c)
        i += 1
    return ''.join(out)


def split_tuple_fields(tuple_body):
    """tuple_body: 괄호 안 내용 (괄호 제외). 최상위 콤마로 필드 분리."""
    fields = []
    cur = []
    in_string = False
    escape = False
    for ch in tuple_body:
        if in_string:
            cur.append(ch)
            if escape:
                escape = False
            elif ch == '\\':
                escape = True
            elif ch == "'":
                in_string = False
            continue
        else:
            if ch == "'":
                in_string = True
                cur.append(ch)
            elif ch == ',':
                fields.append(''.join(cur).strip())
                cur = []
            else:
                cur.append(ch)
    if cur:
        fields.append(''.join(cur).strip())
    return fields


def parse_field(field):
    """필드 문자열을 파이썬 값으로 변환. 'NULL' -> None, '...'-> str, 숫자 -> 그대로(str)."""
    field = field.strip()
    if field == 'NULL':
        return None
    if field.startswith("'") and field.endswith("'"):
        inner = field[1:-1]
        return unescape_mysql_string(inner)
    return field


def iter_insert_tuples(sql_text, table_name):
    """`INSERT INTO `table_name` (...) VALUES (...),(...)...;` 형태의 모든 INSERT 문에서
    튜플들을 yield. (각 행이 별도의 INSERT 문으로 되어 있는 덤프도 지원)"""
    marker = f"INSERT INTO `{table_name}`"
    n = len(sql_text)
    search_from = 0
    while True:
        start = sql_text.find(marker, search_from)
        if start == -1:
            return
        values_start = sql_text.find('VALUES', start)
        pos = sql_text.find('(', values_start)
        while pos < n:
            if sql_text[pos] != '(':
                pos += 1
                continue
            depth = 1
            i = pos + 1
            in_string = False
            escape = False
            while i < n and depth > 0:
                ch = sql_text[i]
                if in_string:
                    if escape:
                        escape = False
                    elif ch == '\\':
                        escape = True
                    elif ch == "'":
                        in_string = False
                else:
                    if ch == "'":
                        in_string = True
                    elif ch == '(':
                        depth += 1
                    elif ch == ')':
                        depth -= 1
                i += 1
            tuple_body = sql_text[pos + 1:i - 1]
            yield tuple_body
            # 다음 '(' 또는 ';' 찾기
            j = i
            while j < n and sql_text[j] in ' \t\r\n,':
                j += 1
            if j >= n or sql_text[j] == ';':
                search_from = j
                break
            pos = j
