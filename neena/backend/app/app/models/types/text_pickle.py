from sqlalchemy import PickleType, Text

class TextPickleType(PickleType):
    impl = Text