#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/11/23
from django.forms import ModelForm
from arya.service import v1
from . import models


class HostInfoModelForm(ModelForm):
    """
    HostInfo表Model
    """

    class Meta:
        model = models.HostInfo
        exclude = ['create_time', 'update_time']


class HostInfoConfig(v1.AryaConfig):
    """
    自定义主机信息展示UI
    """
    model_form_class = HostInfoModelForm
    list_display = ['hostname', 'business', 'idc', 'os', 'cpu', 'mem', 'disk', 'status', 'owner']
    search_list = ['hostname__contains', 'owner__contains']

    def multi_init(self, request):
        """
        批量初始化
        :param request:
        :return:
        """
        print("正在初始化...")
        print(request.POST.getlist('pk'))
        pass

    multi_init.text = "批量初始化"

    def multi_delete(self, request):
        """
        批量删除
        :param request:
        :return:
        """
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list).delete()

    multi_delete.text = "批量删除"

    actions = [multi_init, multi_delete]


class BusiNessConfig(v1.AryaConfig):
    """
    自定义业务线展示UI
    """
    list_display = ['title']
    search_list = ['title__contains']


v1.site.register(models.HostInfo, HostInfoConfig)
v1.site.register(models.BusiNess, BusiNessConfig)
