# Notes 

# Assumptions in the implementation of the FANAP API

1. Add Role: Don't allow role with duplicate attribute name
1. Add Role: Basic Device Role: If field is not determined in role, consider N/A as permission
1. Add Role: Badic Device Role: Only consider RW and NA roles for device
1. List Role: Search for exact deviceTypeId mach when is provided
1. Update Role: Don't allow changing basic device-role (name=device) (error MNC-M013 is used)
1. Device Add: Define new error to prevent adding a device without basic-role (MNC-M119)
1. Role Grant: Generate error when role-grant is repeated
1. Update Role: Permission list will replace whole role permissions
1. Role Grand List: Use username as userid in return list
1. Device Show/Edit, Role Grant: Use MNC-M008 instead of MNC-M016
1. Start first page from 1, return "pageCnt" shows number of pages
1. Device List: isOwned is not supported in Sortby
1. (DONE) Device Show: Only show owned devices
1. Use error MNC-M002 when devicedata parameters are not correct (based on devicetype) 
1. DeviceData Write/Send: Use MNC-M001 when using wrong fields (metadata/data)
1. Requesting a device read by sending "?" is not supported
1. Use "User access denied" when user has no access for read/write one field
1. Device owner has full access for read/write/send

## ToDo

- (DONE) pagination is not supported for role-list yet
- (DONE) Sortby is not supported yet (for role-list )
- ForceUpdate for role-update is not supported yet
- ForceDelete for role-delete is not supported yet
- Update readme.md
- Add create-db script (create databse for first-time)
- (DONE) Now database is created in app/plat1.db, place it in root folder
    and prepare command line arguemnt for user location
- (DONE) Validate device-type fields for duplicate entries
- Implement correct delete (delete orphan related objects)
- Check minimum size for strings (name, role, ....)
- Create script for adding real-world data in database (at startup)
- (Done) ENC is not supported yet
- Overwrite server configurations from os-variables
- Put tests from check_basic.py in separate files

## Issues
- Wired behaviour when using "_" for filtering name in XX-List operations
