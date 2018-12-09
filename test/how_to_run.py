coverage run --source=../app test_devtype_dev_role.py; coverage html



coverage run -a --source=../app test_devtype_dev_role.py
coverage run -a --source=../app test_data.py 
coverage run -a --source=../app test_ddmodel.py 
coverage html

