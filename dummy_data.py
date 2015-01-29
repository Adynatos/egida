from app.models import *


#Room states
for state in ['rented', 'reserved', 'avaliable', 'need_cleaning', 'need_repair']:
    db.session.add(Room_state(state_name=state))
db.session.commit()

#Room types
for r_type in [2, 3, 4]:
    db.session.add(Room_type(r_type=r_type))
db.session.commit()

# Add some rooms

db.session.add(Room(number=1,floor=1,room_type=Room_type.query.filter_by(r_type=2).first(),price_per_day=100,room_state=Room_state.query.filter_by(state_name='avaliable').first()))
db.session.commit()

# Add sex
for sex in ['male', 'female', 'other', 'yes please']:
    db.session.add(Sex(name=sex))
db.session.commit()

