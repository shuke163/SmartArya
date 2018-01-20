#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/12/31

from arya.service import v1
from . import models


class UserConfig(v1.AryaConfig):
    list_display = ['username', ]


v1.site.register(models.User, UserConfig)


class RoleConfig(v1.AryaConfig):
    list_display = ['title', ]


v1.site.register(models.Role, RoleConfig)


class PermissionConfig(v1.AryaConfig):
    list_display = ['title', ]


v1.site.register(models.Permission, PermissionConfig)


class GroupConfig(v1.AryaConfig):
    list_display = ['caption', ]


v1.site.register(models.Group, GroupConfig)


class MenuConfig(v1.AryaConfig):
    list_display = ['title', ]


v1.site.register(models.Menu, MenuConfig)
