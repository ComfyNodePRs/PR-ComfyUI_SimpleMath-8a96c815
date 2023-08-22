import ast
import math
import re
import operator as op

operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Pow: op.pow,
    #ast.BitXor: op.xor,
    #ast.USub: op.neg,
    ast.Mod: op.mod,
}

class SimpleMath:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "a": ("FLOAT", { "default": 0.0, "step": 1 }),
                "b": ("FLOAT", { "default": 0.0, "step": 1 }),
            },
            "required": {
                "value": ("STRING", { "multiline": False, "default": "" }),
            },
        }

    RETURN_TYPES = ("INT", "FLOAT", )

    FUNCTION = "do_math"

    CATEGORY = "utils"

    def do_math(self, value, a = 0.0, b = 0.0):
        def eval_(node):
            if isinstance(node, ast.Num): # number
                return node.n
            elif isinstance(node, ast.Name): # variable
                if node.id == "a":
                    return a
                if node.id == "b":
                    return b
            elif isinstance(node, ast.BinOp): # <left> <operator> <right>
                return operators[type(node.op)](eval_(node.left), eval_(node.right))
            elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
                return operators[type(node.op)](eval_(node.operand))
            else:
                return 0

        result = eval_(ast.parse(value, mode='eval').body)

        if math.isnan(result):
            result = 0.0

        return (round(result), result, )

NODE_CLASS_MAPPINGS = {
    "SimpleMath": SimpleMath
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SimpleMath": "Math op"
}
