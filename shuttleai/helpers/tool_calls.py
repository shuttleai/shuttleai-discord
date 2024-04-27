import inspect
import re
from typing import Callable, Literal, get_type_hints


def _get_type_name(t):
    name = str(t)
    if "list" in name or "dict" in name:
        return name
    else:
        return t.__name__

def serialize_function_to_json(func: Callable) -> dict:
    signature = inspect.signature(func)
    type_hints = get_type_hints(func)
    params = signature.parameters

    function_info = {
        "name": func.__name__,
        "description": func.__doc__.split(":param")[0].strip() if func.__doc__ else "Lorem ipsum...",
        "parameters": {
            "type": "object",
            "properties": {},
        }
    }

    docstring = func.__doc__ or ""
    param_desc_pattern = r":param\s+(\w+)\s*:(.*?)(?=:param|$)"
    param_descriptions = dict(re.findall(param_desc_pattern, docstring, re.DOTALL))

    required_params = [name for name, param in params.items() if param.default == inspect.Parameter.empty]
    if required_params:
        function_info["parameters"]["required"] = required_params

    for name, param in params.items():
        param_type = _get_type_name(type_hints.get(name, type(None)))
        param_desc = param_descriptions.get(name, "Lorem ipsum...").strip()
        if param_type == "Literal":
            function_info["parameters"]["properties"][name] = {
                "type": "string",
                "enum": [literal for literal in type_hints[name].__args__],
                "description": param_desc
            }
        else:
            function_info["parameters"]["properties"][name] = {
                "type": param_type,
                "description": param_desc
            }

    return function_info

def deserialize_function_from_json(json_obj: dict) -> Callable:
    func_name = json_obj["name"]
    func_docstring = json_obj["description"]

    param_types = {}
    param_docstrings = {}
    for param_name, param_info in json_obj["parameters"]["properties"].items():
        param_type = param_info["type"]
        if param_type == "string" and "enum" in param_info:
            param_types[param_name] = Literal[tuple(param_info["enum"])]
        else:
            param_types[param_name] = eval(param_type)
        param_docstrings[param_name] = param_info["description"]

    param_docstring = "\n".join([f":param {name}: {desc}" for name, desc in param_docstrings.items()])
    full_docstring = f"{func_docstring}\n{param_docstring}"

    def func(*args, **kwargs):
        real_func = globals()[func_name]
        return real_func(*args, **kwargs)

    func.__name__ = func_name
    func.__doc__ = full_docstring
    func.__annotations__ = param_types

    return func