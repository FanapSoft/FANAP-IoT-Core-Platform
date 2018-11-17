from marshmallow import Schema, fields

# Place all parameters validation for endpoints


class DeviceType_List(Schema):
    name = fields.String()
    sortBy = fields.String(validate=lambda x: x in ['id', 'name'])
    pageNumber = fields.Integer(default=1)
    pageSize = fields.Integer(default=20)


class Device_List(Schema):
    name = fields.String()
    isOwned = fields.Boolean()
    sortBy = fields.String(validate=lambda x: x in ['id', 'name', 'isOwned'])
    pageNumber = fields.Integer(default=1)
    pageSize = fields.Integer(default=20)


class Role_List(Schema):
    name = fields.String()
    deviceTypeId = fields.String()
    sortBy = fields.String(validate=lambda x: x in [
                           'id', 'name', 'deviceTypeName', 'deviceTypeId'])
    pageNumber = fields.Integer(default=1)
    pageSize = fields.Integer(default=20)


class Role_Delete(Schema):
    forceDelete = fields.Boolean()


class RoleGrant_List(Schema):
    deviceId = fields.String()
    username = fields.String()
    roleId = fields.String()
    sortBy = fields.String(validate=lambda x: x in [
                           'deviceTypeName',
                           'deviceName',
                           'roleName',
                           'username'])


params_schema_dict = dict(
    devicetype_list=DeviceType_List,
    device_list=Device_List,
    role_list=Role_List,
    role_delete=Role_Delete,
    rolegrant_list=RoleGrant_List,
)
