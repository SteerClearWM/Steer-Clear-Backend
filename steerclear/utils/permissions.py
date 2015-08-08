from flask.ext.principal import Permission, RoleNeed
from collections import namedtuple
from functools import partial

# Permission requiring that User must be admin to access resource
admin_permission = Permission(RoleNeed('admin'))

# Permission requiring User to be student to access resource
student_permission = Permission(RoleNeed('student'))

# create Need for only allowing Users to access Rides they request
RideNeed = namedtuple('ride', ['method', 'value'])
AccessRideNeed = partial(RideNeed, 'access')

"""
AccessRidePermission
--------------------
Permission for a specific Ride object.
Used so that Users can only access Rides they requested
"""
class AccessRidePermission(Permission):
	def __init__(self, ride_id):
		need = AccessRideNeed(unicode(ride_id))
		super(AccessRidePermission, self).__init__(need)



