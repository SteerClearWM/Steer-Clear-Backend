import sys, os

# change path to parent directory to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from steerclear import db

if __name__ == "__main__":


	db.drop_all()
	db.create_all()