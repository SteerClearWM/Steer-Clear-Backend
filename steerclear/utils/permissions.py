from flask.ext.principal import Permission, RoleNeed


admin_permission = Permission(RoleNeed('admin'))
student_permission = Permission(RoleNeed('student'))
student_or_admin_permission = Permission(RoleNeed('student'), RoleNeed('admin'))