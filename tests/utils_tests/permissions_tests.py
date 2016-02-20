from tests.base import base
from steerclear.models import User

"""
SteerClearPermissionsTestCase
-----------------------
TestCase for testing permissions
"""
class SteerClearPermissionsTestCase(base.SteerClearBaseTestCase):

    """
    setUp
    -----
    called before each test function. creates new test database
    """
    def setUp(self):
        super(SteerClearPermissionsTestCase, self).setUp()

    """
    test_multiple_users_can_have_student_permission
    -----------------------------------------------
    Tests that multiple users can have the student permission
    """
    def test_multiple_users_can_have_student_permission(self):
        # create new users and give all of them the student permission
        student1 = self._create_user(username='bob', phone='+15554443333', role=self.student_role)
        student2 = self._create_user(username='kat', phone='+12223334445', role=self.student_role)
        student3 = self._create_user(username='ron', phone='+12223334446', role=self.student_role)
        students = [student1, student2, student3]

        # Check that each user has the student permission
        for student in students:
            self.assertIn(self.student_role, student.roles)

    """
    test_multiple_users_can_have_admin_permission
    -----------------------------------------------
    Tests that multiple users can have the admin permission
    """
    def test_multiple_users_can_have_admin_permission(self):
        # create new users and give all of them the student permission
        admin1 = self._create_user(username='bob', phone='+15554443333', role=self.admin_role)
        admin2 = self._create_user(username='kat', phone='+12223334445', role=self.admin_role)
        admin3 = self._create_user(username='ron', phone='+12223334446', role=self.admin_role)
        admins = [admin1, admin2, admin3]

        # Check that each user has the admin permission
        for admin in admins:
            self.assertIn(self.admin_role, admin.roles)

