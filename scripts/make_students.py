

import sys, os

# change path to parent directory to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from steerclear import db
from steerclear.models import User, Role
from sqlalchemy import exc


def main():

    student_role = Role.query.filter_by(name='student').first()
    if student_role is None:
        print "Error: Role does not exist. Start app once and make request"
        sys.exit(0)

    for user in User.query.all():
        if student_role not in user.roles:
            user.roles.append(student_role)

    db.session.commit()


if __name__ == '__main__':
    main()





