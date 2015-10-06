
from schematics import types as t
from schematics.models import Model


class UpdateItemIn(Model):

    tz_offset = t.IntType(required=True)
    uid = t.StringType(required=True)
    what = t.StringType(required=True, max_length=255)
    when = t.DateTimeType(required=True)


class ItemListIn(Model):

    tz_offset = UpdateItemIn.tz_offset
    day = t.DateType(required=False)


class SaveItemIn(Model):

    tz_offset = UpdateItemIn.tz_offset
    what = UpdateItemIn.what
    when = t.DateTimeType(required=False)


class DeleteItemIn(Model):

    uid = UpdateItemIn.uid


class UndoDeleteItemIn(Model):

    uid = UpdateItemIn.uid
