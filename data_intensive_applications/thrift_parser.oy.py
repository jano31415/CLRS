class SchemaError(Exception):
    pass


# not a full parser and not really binary format but i think i got the idea.
class ThriftParser:
    def __init__(self, schema: dict):
        self.schema = schema
        self.type_dict = {str: "b", int: "a", list: "f"}
        self.type_dict_rev = {"b": str, "a": int, "f": list}
        self.pointer = 0

    def encode(self, d: tuple):
        string_builder = []
        if len(d) != len(self.schema):
            raise SchemaError(
                f"Object has {len(d)} fields  but parser expected: {len(self.schema)}"
            )
        for i in range(len(self.schema)):
            type_class, name = self.schema[i]
            if type_class not in self.type_dict:
                raise ValueError(f"Unsupported type: {type_class}")
            string_builder.append(self.type_dict[type_class])

            if type_class == str:
                if len(d[i]) >= 16:
                    pass  # handle
                string_builder.append(hex(len(d[i])))
                for s in d[i]:
                    string_builder.append(str(ord(s)).rjust(3, "0"))
            elif type_class == int:
                if d[i] >= 16:
                    pass  # handle
                string_builder.append(hex(1))
                string_builder.append(str(hex(d[i])))
            elif type_class == list:
                pass
            else:
                pass  # i think this shouldnt happen
        return "".join(string_builder)

    def decode(self, binstr: str):
        obj = {}
        self.pointer = 0
        for i in range(len(self.schema)):
            type_enc = self._get_next(binstr=binstr, size=1)
            type_class = self.type_dict_rev[type_enc]  # handle unknown type
            type_len = int(self._get_next(binstr=binstr, size=3), 16)
            if type_class == str:
                sb = []
                for j in range(type_len):
                    sb.append(chr(int(self._get_next(binstr=binstr, size=3))))
                # int/list
                obj[self.schema[i][1]] = "".join(sb)
            elif type_class == int:
                value = int(self._get_next(binstr=binstr, size=3), 16)
                obj[self.schema[i][1]] = value
            else:
                pass  # implement more types refactor into methods etc
        # assert self.pointer ==len(bin) ?
        self.pointer = 0
        return obj

    def _get_next(self, binstr: str, size: int):
        res = binstr[self.pointer : self.pointer + size]
        self.pointer += size
        return res


def check_thrift_parser():
    example_schema = [(str, "username"), (int, "favorite_number"), (str, "interests")]
    parser = ThriftParser(schema=example_schema)
    example_object = ("superuser", 14, "abcdef")
    bin = parser.encode(d=example_object)
    parsed_object = parser.decode(bin)
    print(parsed_object)
    assert example_object == tuple(parsed_object.values())
    example_object = ("othername", 7, "yeah")
    bin = parser.encode(d=example_object)
    parsed_object = parser.decode(bin)
    print(parsed_object)
    assert example_object == tuple(parsed_object.values())


check_thrift_parser()
