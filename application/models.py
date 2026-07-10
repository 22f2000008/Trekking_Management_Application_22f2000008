from .database import db
from datetime import datetime

trek_staff = db.Table(
    "trek_staff",
    db.Column("trek_id", db.Integer, db.ForeignKey("treks.id")),
    db.Column("staff_id", db.Integer, db.ForeignKey("users.id"))
)
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False, default="user")
    active = db.Column(db.Boolean, default=True)
    
    # Relationships
    bookings = db.relationship("Booking", backref="user", lazy=True, cascade="all, delete-orphan")
    treks = db.relationship("Trek",secondary=trek_staff,back_populates="staffs")

    def __repr__(self):
        return f"<User {self.username}>"
    
class StaffProfile(db.Model):
    __tablename__ = "staff_profiles"
    id = db.Column(db.Integer(), primary_key=True)
    phone = db.Column(db.String())
    address = db.Column(db.String())
    status = db.Column(db.String(), default="Active")
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), unique=True, nullable=False)
    user = db.relationship("User", backref=db.backref("staff_profile", uselist=False))

    def __repr__(self):
        return f"<StaffProfile {self.id}>"
    
class Trek(db.Model):
    __tablename__ = "treks"
    id = db.Column(db.Integer(), primary_key=True)
    trek_name = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(), nullable=False)
    difficulty = db.Column(db.String(), nullable=False)  
    duration = db.Column(db.Integer(), nullable=False)   
    available_slots = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.Text())
    start_date = db.Column(db.Date(), nullable=False)
    end_date = db.Column(db.Date(), nullable=False)
    status = db.Column(db.String(), default="Pending")    
    
    # Relationships
    bookings = db.relationship("Booking", backref="trek", lazy=True, cascade="all, delete-orphan")
    staffs = db.relationship("User", secondary=trek_staff, back_populates="treks")

    def __repr__(self):
        return f"<Trek {self.trek_name}>"
    

    
class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer(), primary_key=True)
    booking_date = db.Column(db.DateTime(), default=datetime.utcnow)
    status = db.Column(db.String(), default="Booked")   
    payment_status = db.Column(db.String(), default="Pending")
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
    trek_id = db.Column(db.Integer(), db.ForeignKey("treks.id"), nullable=False)

    def __repr__(self):
        return f"<Booking {self.id}>"

