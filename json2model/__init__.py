#! /usr/bin/env python3
import re
import collections
import json
from pathlib import Path
from simpletemplate import Template
import simpletemplate
from typing import NamedTuple, List, Dict
from pyperclip import copy, paste
from termcolor import cprint

simpletemplate.DEBUG_TEMPLATE = False
g_commonPrefix = ""


class JField(NamedTuple):
    j_type: str
    name: str
    raw: str


class JClass(NamedTuple):
    name: str
    fields: List[JField]


def gen_class_name(name: str) -> str:
    if not name:
        return f"{g_commonPrefix}Pojo"
    return f"{g_commonPrefix}{name[0].upper()}{name[1:]}"


def gen_field_name(field: str) -> str:
    return f"m{field[0].upper()}{field[1:]}"


g_class: List[JClass] = []
pojo = JClass("Pojo", [])


def json2pojo(_json, recommand_name: str = None, toplevel=False):
    if isinstance(_json, list) and len(_json) > 0:
        t = json2pojo(_json[0], recommand_name)
        return f"List<{t}>"
    elif isinstance(_json, dict):
        jclass: JClass = pojo if toplevel else JClass(
            gen_class_name(recommand_name), []
        )
        for k, v in _json.items():
            t = json2pojo(v, k)
            jclass.fields.append(JField(t, gen_field_name(k), k))
        if not toplevel:
            g_class.append(jclass)
        return jclass.name
    elif isinstance(_json, bool):
        return "boolean"
    elif isinstance(_json, str):
        return "String"
    elif isinstance(_json, float):
        return "double"
    elif isinstance(_json, int):
        return "int"
    else:
        assert False, f"unknown json type: {_json}"


def serialid():
    import random

    li = [str(random.randrange(0, 10)) for _ in range(19)]
    return "".join(li)


TEMPLATE = r"""\
import java.io.Serializable;
import java.util.List;
import com.google.gson.annotations.SerializedName;

/**
 * xxx
 *
 * @author xxx 
 */
public class {{commonPrefix}}{{pojo.name}} implements Serializable {
    private static final long serialVersionUID = {{serialid()}}L;

%{for f in pojo.fields:}%
    @SerializedName(\"{{f.raw}}\")
    public {{f.j_type}} {{f.name}};
%{end}%

%{for cls in cls_defs:}%
    public static class {{cls.name}} implements Serializable {
        private static final long serialVersionUID = {{serialid()}}L;
%{for f in cls.fields:}%
        @SerializedName(\"{{f.raw}}\")
        public {{f.j_type}} {{f.name}};
%{end}%
    }

%{end}%
}\
"""


def chain(arg, *funcs):
    r = arg
    for f in funcs:
        r = f(r)
    return r


def parse(_json: str) -> Dict:
    if not _json:
        raise SystemExit("empty json", -1)
    try:
        return json.loads(_json)
    except Exception as e:
        print("json:", _json)
        raise SystemExit('invalid json format', -1)


def remove_json_comment(_json: str) -> str:
    return re.sub(r'//[^"}{]*\n', '\n', _json)


def get_json(file: str):
    if not file:
        return paste()
    p = Path(file)
    if p.exists():
        return p.read_text()
    else:
        raise SystemExit(f"file {file} not exists", -1)


def main(prefix: str = "Custom", file: str = None):
    global g_commonPrefix
    g_commonPrefix = prefix

    _json = chain(file,
                  get_json,
                  str.strip,
                  remove_json_comment,
                  parse)

    json2pojo(_json, toplevel=True)

    code = Template(TEMPLATE).render(
        {
            "pojo": pojo,
            "cls_defs": g_class,
            "serialid": serialid,
            "commonPrefix": prefix,
        }
    )
    sep = '=' * 30
    cprint(code, 'yellow')
    cprint(f'{sep} code already copy info clipboard, just paste {sep}', 'green')
    copy(code)