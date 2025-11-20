from .base import LoginConfig, RegisterConfig, ProfileConfig, UsersManagementConfig, SettingsConfig, AuthComponents
from .authpage import AuthPages
from .profilePage import ProfilePages
from .userManager import UsersManagement
from .settings import SettingsPages


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