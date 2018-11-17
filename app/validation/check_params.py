from app.exception import ApiExp
from .param_schema import params_schema_dict


def reqparam_validate(schema_name, data_dict):

    if not schema_name:
        return data_dict

    schema = params_schema_dict[schema_name]()

    chk = schema.load(data_dict)

    if chk.errors:
        raise ApiExp.Parameters(dbg_msg=chk.errors)

    return chk.data
