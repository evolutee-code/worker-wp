from enum import Enum

class UserTypeEnum(Enum):
    super_admin = "super_admin"
    admin = "admin"
    leader = "leader"
    member = "member"
    customer = "customer"
