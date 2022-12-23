from typing import Optional
import json


class PGType:
    """Represents a PostgreSQL type and a function to convert a Python value to its wire format."""

    _instances = {}

    def __init__(self, oid, converter=None):
        if oid in self._instances:
            raise ValueError(f"Duplicate OID {oid} declared for PGType")
        self.oid = oid
        if not converter:
            self.converter = lambda x: str(x)
        else:
            self.converter = converter
        self._instances[oid] = self

    @classmethod
    def find_by_oid(cls, oid: int) -> Optional["PGType"]:
        t = cls._instances.get(oid)
        return PGTypes.UNKNOWN if not t else t


class PGTypes:
    BIGINT = PGType(20)
    BOOL = PGType(16, lambda v: "true" if v else "false")
    BYTES = PGType(17, lambda v: "\\x" + v.hex())
    DATE = PGType(1082, lambda v: v.isoformat())
    FLOAT = PGType(701)
    INTEGER = PGType(23)
    INTERVAL = PGType(
        1186,
        lambda v: f"{v.days} days {v.seconds} seconds {v.microseconds} microseconds",
    )
    JSON = PGType(114, lambda v: json.dumps(v))
    NUMERIC = PGType(1700)
    NULL = PGType(-1, lambda v: None)
    TEXT = PGType(25)
    TIME = PGType(1083, lambda v: v.isoformat())
    TIMESTAMP = PGType(1114, lambda v: v.isoformat().replace("T", " "))
    UNKNOWN = PGType(705)