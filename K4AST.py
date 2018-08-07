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
