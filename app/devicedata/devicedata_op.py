# Check if user if owner of this deviceid or there is a role
# For accessing this device type for the user
#
#
# 1 D Check if user has access to the target device
# 2   Validate attributes based on the devicetype
# 3   Validate fields based on


from app.device import get_by_deviceid_or_404


def devicedata_write(user, data, deviceid, params):

    # Check if any device is assigned to this user:
    device = get_by_deviceid_or_404(user, deviceid, look_in_granted=True)

    devicetype = device.devicetype

    return dict(msg='This is device data write',
                dname=device.name,
                dtname=devicetype.name,
                data=data)


def devicedata_read(user, deviceid, params):
    return dict(msg='This is device data read', deviceid=deviceid)
