#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/11/23
from django.conf.urls import url
from django.shortcuts import render, redirect, HttpResponse
from django.utils.safestring import mark_safe
from django.forms import ModelForm
from django.urls import reverse
from django.db.models import Q
from ..utils.page import Pagination
import copy


class ChangeList(object):
    """
    列表页面所有展示功能处理
    """

    def __init__(self, config, queryset):
        self.config = config  # AryaConfig 对象
        self.list_display = config.get_list_display()
        self.queryset = queryset
        self.show_add = config.get_show_add()
        self.add_url = config.reverse_add_url()
        self.search_list = config.get_search_list()
        self.q_value = config.request.GET.get('q', '')
        self.actions = config.get_actions()

        # 分页
        request = config.request
        query_params = copy.deepcopy(request.GET)  # AueryDict
        current_page = request.GET.get('page', 1)
        per_page = config.per_page
        pager_page_count = config.pager_page_count
        all_count = queryset.count()
        base_url = config.reverse_list_url()
        page_obj = Pagination(current_page, all_count, base_url, query_params, per_page, pager_page_count)
        self.queryset = queryset[page_obj.start:page_obj.end]
        self.page_html = page_obj.page_html()

    def table_header(self):
        """
        表头标题
        :return:
        """
        title = []
        for str_func in self.list_display:
            if isinstance(str_func, str):
                val = self.config.model_class._meta.get_field(str_func).verbose_name
            else:
                val = str_func(self.config, is_header=True)
            title.append(val)
        # print("表头: ", title)
        return title

    def table_body(self):
        """
        table数据内容
        :return:
        """
        table_data = []
        for obj in self.queryset:
            row = []
            for str_func in self.list_display:
                if isinstance(str_func, str):
                    col = getattr(obj, str_func)
                else:
                    col = str_func(self.config, row=obj)
                row.append(col)
            table_data.append(row)
        # print("表数据: ", table_data)
        return table_data

    def action_options(self):
        """
        批量操作
        :return:
        """
        data = []
        for func in self.actions:
            temp = {'value': func.__name__, 'text': func.text}
            data.append(temp)
        return data


class AryaConfig(object):
    """
    每个models类的URL对应处理的View实现
    """

    def __init__(self, model_class, site):
        self.model_class = model_class
        # View 的obj对象
        self.site = site
        # app name
        self.app = self.model_class._meta.app_label
        # models name
        self.md = self.model_class._meta.model_name

    # 1. 列表页展示相关
    list_display = []

    def get_list_display(self):
        """
        列表展示
        :return:
        """
        result = []
        result.extend(self.list_display)
        # 如果有编辑权限
        result.append(AryaConfig.row_edit)
        # 如果有删除权限
        result.append(AryaConfig.row_del)
        # 多选
        result.insert(0, AryaConfig.row_checkbox)
        return result

    def row_checkbox(self, row=None, is_header=None):
        """
        多选
        :param row:
        :param is_header:
        :return:
        """
        if is_header:
            return "选择"
        html = "<input type='checkbox' name='pk' value='{0}' />".format(row.id)
        return mark_safe(html)

    def row_edit(self, row=None, is_header=None):
        """
        编辑
        :param row: row_obj
        :param is_header: 是否是标题
        :return: 编辑HTML
        """
        if is_header:
            return "编辑"
        # app = self.model_class._meta.app_label
        # md = self.model_class._meta.model_name
        name = "arya:{app}_{md}_change".format(app=self.app, md=self.md)
        url = reverse(viewname=name, args=(row.id,))
        html = "<a href='{0}'>编辑</a>".format(url)
        return mark_safe(html)

    def row_del(self, row=None, is_header=None):
        """
        删除
        :param row:
        :param is_header:
        :return: 删除HTML
        """
        if is_header:
            return "删除"
        name = "arya:{app}_{md}_delete".format(app=self.app, md=self.md)
        url = reverse(viewname=name, args=(row.id,))
        html = "<a href='{0}'>删除</a>".format(url)
        return mark_safe(html)

    # 2. 添加按钮相关
    show_add = True

    def get_show_add(self):
        # 如果有增加权限返回True，否则返回False
        return self.show_add

    # 3. ModelForm
    model_form_class = None

    def get_model_form_class(self):
        """
        ModelForm提交数据验证相关
        :return:
        """
        if self.model_form_class:
            return self.model_form_class

        class DynamicModelForm(ModelForm):
            class Meta:
                model = self.model_class
                fields = "__all__"

        return DynamicModelForm

    # 4. 模糊查询
    search_list = []

    def get_search_list(self):
        rest = []
        rest.extend(self.search_list)
        return rest

    # 5. 分页配置
    per_page = 10
    pager_page_count = 11

    # 6. actions
    actions = []

    def get_actions(self):
        """
        批量操作
        :return:
        """
        result = []
        result.extend(self.actions)
        return result

    @property
    def urls(self):
        app = self.model_class._meta.app_label
        md = self.model_class._meta.model_name
        # 增删改查URLS
        partterns = [
            url(r'^$', self.changelist_view, name="{app}_{md}_list".format(app=app, md=md)),
            url(r'^add/', self.add_view, name="{app}_{md}_add".format(app=app, md=md)),
            url(r'^(\d+)/change/$', self.change_view, name="{app}_{md}_change".format(app=app, md=md)),
            url(r'^(\d+)/delete/$', self.delete_view, name="{app}_{md}_delete".format(app=app, md=md))
        ]
        return partterns

    def reverse_add_url(self):
        """
        添加URL路径
        :return: 返回添加URL路径
        """
        name = "arya:{app}_{md}_add".format(app=self.app, md=self.md)
        url = reverse(viewname=name)
        return url

    def reverse_list_url(self):
        """
        列表展示页URL
        :return: 返回列表展示页URL
        """
        name = "arya:{app}_{md}_list".format(app=self.app, md=self.md)
        url = reverse(viewname=name)
        return url

    def changelist_view(self, request):
        """
        列表试图
        :param request:
        :return:
        """
        self.request = request
        # 批量操作
        if request.method == "POST":
            action_item_name = request.POST.get('select_action')
            if action_item_name:
                func = getattr(self, action_item_name)
                func(request)
        # 模糊查询
        contains = Q()
        search_q = request.GET.get('q')
        search_list = self.get_search_list()
        if search_q and search_list:
            for field in search_list:
                temp = Q()
                temp.children.append((field, search_q))
                contains.add(temp, 'OR')

        queryset = self.model_class.objects.filter(contains)

        # 此处的self为AryaConfig对象，对应ChangeList中的config参数
        chlist = ChangeList(self, queryset)

        return render(request, 'arya/changelist_view.html', {'chlist': chlist})

    def add_view(self, request):
        """
        添加试图
        :param request:
        :return:
        """
        model_form_cls = self.get_model_form_class()
        if request.method == "GET":
            form = model_form_cls()
            for item in form:
                print(item)
            return render(request, 'arya/add_view.html', {'form': form})
        else:
            # 添加页面提交数据验证并保存
            form = model_form_cls(data=request.POST)
            if form.is_valid():
                form.save()
                # 返回列表页面
                return redirect(self.reverse_list_url())
            return render(request, 'arya/add_view.html', {'form': form})

    def change_view(self, request, nid):
        """
        修改试图
        :param request:
        :return:
        """
        obj = self.model_class.objects.filter(pk=nid).first()
        if not obj:
            return redirect(self.reverse_list_url())

        model_form_cls = self.get_model_form_class()
        if request.method == "GET":
            # input框中显示默认值
            form = model_form_cls(instance=obj)
            return render(request, 'arya/change_view.html', {'form': form})
        else:
            # 更新数据
            form = model_form_cls(instance=obj, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.reverse_list_url())
            return render(request, 'arya/change_view.html', {'form': form})

    def delete_view(self, request, nid):
        """
        删除试图
        :param request:
        :return:
        """
        obj = self.model_class.objects.filter(pk=nid).first()
        if not obj:
            return redirect(self.reverse_list_url())
        if request.method == "GET":
            return render(request, 'arya/delete_view.html')
        else:
            obj.delete()
            return redirect(self.reverse_list_url())


class AryaSite(object):
    """
    实现类似于admin.site.register()功能
    """

    # 存放所有的models类及对应处理UTRL的的view对象
    def __init__(self):
        self._registry = {}

    def register(self, class_name, config_class):
        """
        注册方法,封装对象
        self._registry = {
            module.UserInfo: obj1,  # obj1 = AryaConfig(models.UserInfo,site),
            module.UserType: obj2,  # obj2 = AryaConfig(models.UserType,site),
        }
        :param class_name: models类
        :param config_class: 对应的View类(AryaConfig)
        :return:
        """
        self._registry[class_name] = config_class(class_name, self)

    @property
    def urls(self):
        """
        处理子路由
        :return:
        """
        partterns = [
            url(r'^login/$', self.login),
            url(r'^logout/$', self.logout),
        ]
        # 循环self._registry属性里面的每一个元素，key为models类，value为URLS对应处理的类obj对象
        for model_class, arya_config_obj in self._registry.items():
            # 分别为app名称和models的类名称
            # print("*" * 50)
            # print(model_class._meta.app_label, model_class._meta.model_name)
            app_model_name_urls = r'^{0}/{1}/'.format(model_class._meta.app_label, model_class._meta.model_name)
            # arya_config_obj.urls self._registry字典中存放的values对象obj下面的urls方法
            pt = url(app_model_name_urls, (arya_config_obj.urls, None, None))
            partterns.append(pt)

        return partterns

    def login(self):
        """
        登陆
        :return:
        """
        return redirect('login')

    def logout(self):
        """
        退出
        :return:
        """
        return redirect('login')


# 实例化，利用单例模式
site = AryaSite()
