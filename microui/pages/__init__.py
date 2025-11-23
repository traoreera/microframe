from .authpage import AuthPages
from .base import (
    AuthComponents,
    LoginConfig,
    ProfileConfig,
    RegisterConfig,
    SettingsConfig,
    UsersManagementConfig,
)
from .profilePage import ProfilePages
from .settings import SettingsPages
from .userManager import UsersManagement

__all__ = [
    "LoginConfig",
    "RegisterConfig",
    "ProfileConfig",
    "UsersManagementConfig",
    "SettingsConfig",
    "AuthComponents",
    "AuthPages",
    "ProfilePages",
    "UsersManagement",
    "SettingsPages",
]


__annotations__ = {
    "LoginConfig": LoginConfig,
    "RegisterConfig": RegisterConfig,
    "ProfileConfig": ProfileConfig,
    "UsersManagementConfig": UsersManagementConfig,
    "SettingsConfig": SettingsConfig,
    "AuthComponents": AuthComponents,
    "AuthPages": AuthPages,
    "ProfilePages": ProfilePages,
    "UsersManagement": UsersManagement,
    "SettingsPages": SettingsPages,
}
