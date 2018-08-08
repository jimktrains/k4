class Record:
    name = None
    definitions = None

    def __init__(self, name, definitions):
        self.name = name
        self.definitions = definitions

    def __repr__(self):
        return self.format('')

    def format(self, prefix):
        x = prefix + "Record(" + self.name + "):\n"
        for definition in self.definitions:
            x += definition.format(prefix + "\t") + "\n"
        return x

class Definition:
    v_type = None
    name = None

    def __init__(self, v_type, name):
        self.v_type = v_type
        self.name = name

    def __repr__(self):
        return self.format('')

    def format(self, prefix):
        return prefix + str(self.v_type) + " " + self.name

class Module:
    name = None
    statements = []

    def __init__(self, name, statements):
        self.name = name
        self.statements = statements

    def __repr__(self):
        return self.format('')

    def format(self, prefix):
        x = "Module(" + self.name + "):\n" 
        for statement in self.statements:
            x += statement.format(prefix + "\t")
        return x

class Enum:
    name = None
    storage_type = None
    values = []

    def __init__(self, name, storage_type, values):
        self.name = name
        self.storage_type = storage_type
        self.values = values

    def __repr__(self):
        return self.format('')

    def format(self, prefix):
        x = prefix + "Enum(" + self.name + ")<" + self.storage_type + ">:\n" 
        for value in self.values:
            x += value.format(prefix + "\t") + "\n"
        return x

class EnumValue:
    name = None
    value = None

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return self.format('')

    def format(self, prefix):
        return prefix + str(self.name) + " := " + repr(self.value)

class Number:
    value = None

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.format('')

    def format(self, prefix):
        return prefix + str(self.value)

class Type:
    value = None

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.format('')

    def format(self, prefix):
        return prefix + str(self.value)
