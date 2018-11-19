
class PermissionList:
    ReadBit = 1
    WriteBit = 2

    def __init__(self, fields_name):
        self.permissions = {
            x: 0 for x in fields_name
        }

    def access_all(self):
        self.permissions = {x: (self.ReadBit+self.WriteBit)
                            for x in self.permissions}

    def _p2rw(self, val):
        ret = ''
        if val & PermissionList.ReadBit:
            ret = ret+'R'

        if val & PermissionList.WriteBit:
            ret = ret + 'W'

        if not ret:
            ret = 'N'
        return ret

    def _rw2p(self, per_str):
        per_str = str.upper(per_str)

        v = 0
        if 'R' in per_str:
            v = v | PermissionList.ReadBit

        if 'W' in per_str:
            v = v | PermissionList.WriteBit

        return v

    def __repr__(self):
        return " ".join([
            '{}={}'.format(n, self._p2rw(v))
            for n, v in self.permissions.items()
        ])

    def or_by_permission_dict(self, data):
        for field, per_str in data.items():
            v = self._rw2p(per_str)

            if field in self.permissions:
                self.permissions[field] |= v

    def check_read_access(self, field_list):
        return self.check_access(field_list, write_check=False)

    def check_write_access(self, field_list):
        return self.check_access(field_list, write_check=True)

    def check_access(self, field_list, write_check=True):
        mask = (PermissionList.WriteBit if write_check else
                PermissionList.ReadBit)
        for f in field_list:
            if f not in self.permissions:
                return False

            if not (self.permissions[f] & mask):
                return False
        return True

    def get_fields_with_read_permission(self):
        mask = PermissionList.ReadBit
        return [n for n, p in self.permissions.items() if p & mask]
