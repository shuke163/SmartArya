from django.db import models


class HostInfo(models.Model):
    """
    主机信息表
    """
    hostname = models.CharField(max_length=64, verbose_name="主机名")
    business = models.ForeignKey(to="BusiNess", blank=True, verbose_name="所属业务线")
    idc = models.CharField(max_length=32, verbose_name="机房")
    os = models.CharField(max_length=16, verbose_name="OS")
    cpu = models.CharField(max_length=16, verbose_name="CPU")
    mem = models.CharField(max_length=16, verbose_name="MEM")
    disk = models.CharField(max_length=16, verbose_name="DISK")
    status = models.CharField(max_length=16, verbose_name="状态")
    owner = models.CharField(max_length=16, verbose_name="负责人")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="更新时间")

    class Meta:
        verbose_name_plural = "主机表"

    def __str__(self):
        return self.hostname


class BusiNess(models.Model):
    """
    业务线
    """
    title = models.CharField(max_length=32, verbose_name="业务线")

    class Meta:
        verbose_name_plural = "业务线"

    def __str__(self):
        return self.title

# data = []
# for i in range(150):
#     obj = HostInfo(hostname="dkr%s.com.cn" % str(i), business_id=2, idc="ali-cloud", os="centos 6.8_x64",
#                    cpu="%sc" % str(i), mem="%sG" % str(i), disk="%dG" % i, status="online", owner="shuke")
#     data.append(obj)
#
# HostInfo.objects.bulk_create(data)