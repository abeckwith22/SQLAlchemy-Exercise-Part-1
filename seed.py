"""Seed file to make sample data for users db."""
from models import User, db
from app import app

app.app_context().push()

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it 
User.query.delete()

# Add users
QuantumQuasar23 = User(first_name='Alan', last_name='Alda')
VelvetVortex56 = User(first_name='Joel', last_name='Burton')
NimbusNebula77 = User(first_name='Jane', last_name='Smith')

# Adding users to db
db.session.add(QuantumQuasar23)
db.session.add(VelvetVortex56)
db.session.add(NimbusNebula77)

#  Commiting users to db
db.session.commit()
