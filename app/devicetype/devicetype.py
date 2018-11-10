


def devicetype_add(user, payload, params):
    return dict(user=user, payload=payload, params = params)

    # def process_devicetype_add(self, user, payload, params):
    #     payload_ok, payload_chk_msg = self.json_validator.check_devicetype_add(payload)

    #     if not payload_ok:
    #         return self.get_json_structure_error(dbg_msg=payload_chk_msg)

    #     # Check if device-type with same name exists
    #     table = self.db.get_table('devicetype')


    #     if table.find_one(name=payload['name'], user=user):
    #         return self.get_json_duplicate_devicetype_error()

    #     new_devtype_id = self._get_unique_devicetypeid()

    #     description = payload.get('description', '')

    #     table.insert( dict(
    #         name = payload['name'],
    #         enc_en = payload['encryptionEnabled'],
    #         description = description,
    #         user = user,
    #         devicetypeid= new_devtype_id,
    #         devicetype = json.dumps(dict(data=payload['attributeTypes'])),
    #         role = '', # Basic devicetype role (determine which field is meta-data)
    #         ))


    #     return dict(
    #         timestamp=time.time(),  
    #         message = self._generate_message_dict(Platform.MSG_OK), 
    #         data = {"id":new_devtype_id},
    #         )
