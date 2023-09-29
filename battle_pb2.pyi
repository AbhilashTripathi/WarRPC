from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InitReq(_message.Message):
    __slots__ = ["N", "T"]
    N_FIELD_NUMBER: _ClassVar[int]
    T_FIELD_NUMBER: _ClassVar[int]
    N: int
    T: int
    def __init__(self, N: _Optional[int] = ..., T: _Optional[int] = ...) -> None: ...

class MissileNotification(_message.Message):
    __slots__ = ["t", "missile_type", "x", "y"]
    T_FIELD_NUMBER: _ClassVar[int]
    MISSILE_TYPE_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    t: int
    missile_type: str
    x: int
    y: int
    def __init__(self, t: _Optional[int] = ..., missile_type: _Optional[str] = ..., x: _Optional[int] = ..., y: _Optional[int] = ...) -> None: ...

class TrackingDetails(_message.Message):
    __slots__ = ["casualty_count", "soldier_count"]
    CASUALTY_COUNT_FIELD_NUMBER: _ClassVar[int]
    SOLDIER_COUNT_FIELD_NUMBER: _ClassVar[int]
    casualty_count: int
    soldier_count: int
    def __init__(self, casualty_count: _Optional[int] = ..., soldier_count: _Optional[int] = ...) -> None: ...

class SoldierDetail(_message.Message):
    __slots__ = ["id", "x", "y", "speed", "status", "is_commander"]
    ID_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    IS_COMMANDER_FIELD_NUMBER: _ClassVar[int]
    id: int
    x: int
    y: int
    speed: int
    status: str
    is_commander: bool
    def __init__(self, id: _Optional[int] = ..., x: _Optional[int] = ..., y: _Optional[int] = ..., speed: _Optional[int] = ..., status: _Optional[str] = ..., is_commander: bool = ...) -> None: ...

class InitDetails(_message.Message):
    __slots__ = ["sol_details"]
    SOL_DETAILS_FIELD_NUMBER: _ClassVar[int]
    sol_details: _containers.RepeatedCompositeFieldContainer[SoldierDetail]
    def __init__(self, sol_details: _Optional[_Iterable[_Union[SoldierDetail, _Mapping]]] = ...) -> None: ...
