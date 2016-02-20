import sys, os

# change path to parent directory to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from steerclear import db
from steerclear.models import Role

if __name__ == "__main__":


    db.drop_all()
    db.create_all()
    

    student_role = Role(name='student', description='Student Role')
    admin_role = Role(name='admin', description='Admin Role')
    db.session.add_all([student_role, admin_role])
    db.session.commit()

