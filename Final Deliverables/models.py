from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, IntEnum


class Language(Enum):
    English = "en"
    French = "fr"
    Russian = "ru"
    Japanese = "ja"
    Chinese = "zh"
    Spanish = "es"


class TicketStatus(Enum):
    OPEN = 1
    CLOSED = 2
    IN_PROGRESS = 3


class TicketPrio(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Ticket:
    uid: str
    author: User
    title: str
    description: str
    priority: TicketPrio
    status: TicketStatus

    @classmethod
    def from_tuple(cls, user, ticket_details):
        uid = ticket_details[0]
        title = ticket_details[2]
        desc = ticket_details[3]
        prio = TicketPrio[ticket_details[4]]
        status = TicketStatus[ticket_details[5]]
        ticket = cls(uid, user, title, desc, prio, status)
        return ticket


@dataclass
class User:
    uid: str
    name: str
    email: str
    password: str
    role: UserType
    language: Language = Language.English

    @classmethod
    def from_tuple(cls, user_data):
        user_data[-1] = Language[user_data[-1]]
        user_data[-2] = UserType[user_data[-2]]
        user = cls(*user_data)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.uid)


class UserType(IntEnum):
    ANY = 0
    CUSTOMER = 1
    AGENT = 2
    ADMIN = 3
