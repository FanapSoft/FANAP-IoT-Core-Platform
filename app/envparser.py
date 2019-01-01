import os
import environs

# Helper function for updating configuration dictionary using OS env variables

def build(cfg_pattern):
    # Format of the cfg_pattern [(name, default_value='', type='str'), ....]
    env = environs.Env()

    parser_dict = dict(
        str=env.str,
        bool=env.bool,
        int=env.int
    )

    ret = {}

    for cfg in cfg_pattern:
        name, def_value, p_type, *_ = tuple(cfg) + (('', 'str') if len(cfg)==1 else ('str',))
        parser = parser_dict[p_type]

        ret[name] = parser(name, def_value)

    return ret