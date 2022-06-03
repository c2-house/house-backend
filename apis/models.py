from django.db import models


class BaseModel(models.Model):
    supply_type = models.CharField(max_length=10, verbose_name="공급유형")
    title = models.CharField(max_length=255, verbose_name="공고명")
    registration_date = models.DateField(verbose_name="모집공고 일자")
    supplier = models.CharField(max_length=50, verbose_name="공급 기관")
    link = models.URLField(verbose_name="링크")

    class Meta:
        abstract = True


class SH(models.Model):
    ...


class MyHome(BaseModel):
    status = models.BooleanField(verbose_name="진행상태")
    region = models.CharField(max_length=10, verbose_name="지역")
    release_date = models.DateField(verbose_name="당첨발표 일자")


class StationArea(BaseModel):
    index = models.PositiveIntegerField(verbose_name="인덱스")
    apply_date = models.DateField(verbose_name="청약신청일")
