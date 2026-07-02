from flask import current_app as app
from flask import request, jsonify

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from .models import User,StaffProfile,Trek, Booking
from .database import db
from datetime import datetime


# =====================================
# REGISTER
# =====================================

@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({
            "message": "All fields are required"
        }), 400

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return jsonify({
            "message": "Email already registered"
        }), 409

    user = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        role="user"
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully"
    }), 201


# =====================================
# LOGIN
# =====================================

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        return jsonify({
            "message": "Wrong email or password"
        }), 401
    
    if not user.active:
        return jsonify({
            "message": "Account is deactivated"
        }), 403

    if not check_password_hash(
        user.password,
        password
    ):
        return jsonify({
            "message": "Wrong email or password"
        }), 401

    access_token = create_access_token(
        identity=user
    )

    return jsonify({
        "access_token": access_token,
        "username": user.username,
        "role": user.role
    }), 200


# =====================================
# PROFILE
# =====================================

@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "active": current_user.active
    }), 200


@app.route("/admin/staff", methods=["POST"])
@jwt_required()
def create_staff():

    # Only admin can create staff
    if current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    address = data.get("address")

    if not username or not email or not password:
        return jsonify({
            "message": "All fields are required"
        }), 400

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return jsonify({
            "message": "Email already exists"
        }), 409

    # Create user with role = staff
    staff_user = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        role="staff"
    )

    db.session.add(staff_user)
    db.session.commit()

    # Create staff profile
    staff_profile = StaffProfile(
        phone=phone,
        address=address,
        user_id=staff_user.id
    )

    db.session.add(staff_profile)
    db.session.commit()

    return jsonify({
        "message": "Staff created successfully"
    }), 201



@app.route("/admin/users", methods=["GET"])
@jwt_required()
def get_users():

    if current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    users = User.query.filter_by(role="user").all()

    result = []

    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "active": user.active
        })

    return jsonify(result), 200


@app.route("/admin/staff", methods=["GET"])
@jwt_required()
def get_staff():

    if current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    staffs = User.query.filter_by(role="staff").all()

    result = []

    for staff in staffs:
        result.append({
            "id": staff.id,
            "username": staff.username,
            "email": staff.email,
            "active": staff.active
        })

    return jsonify(result), 200


@app.route("/admin/treks", methods=["POST"])
@jwt_required()
def create_trek():

    if current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    data = request.get_json()

    trek = Trek(
        trek_name=data.get("trek_name"),
        location=data.get("location"),
        difficulty=data.get("difficulty"),
        duration=data.get("duration"),
        available_slots=data.get("available_slots"),
        description=data.get("description"),
        start_date=datetime.strptime(
            data.get("start_date"),
            "%Y-%m-%d"
        ).date(),
        end_date=datetime.strptime(
            data.get("end_date"),
            "%Y-%m-%d"
        ).date(),
        status="Pending"
    )

    db.session.add(trek)
    db.session.commit()

    return jsonify({
        "message": "Trek created successfully"
    }), 201

@app.route("/admin/treks", methods=["GET"])
@jwt_required()
def get_treks():

    if current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    treks = Trek.query.all()

    result = []

    for trek in treks:
        result.append({
            "id": trek.id,
            "trek_name": trek.trek_name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "available_slots": trek.available_slots,
            "status": trek.status
        })

    return jsonify(result), 200

@app.route("/admin/assign-staff/<int:trek_id>", methods=["PUT"])
@jwt_required()
def assign_staff(trek_id):

    if current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    data = request.get_json()

    staff_id = data.get("staff_id")

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "message": "Trek not found"
        }), 404

    staff = User.query.filter_by(
        id=staff_id,
        role="staff"
    ).first()

    if not staff:
        return jsonify({
            "message": "Staff not found"
        }), 404

    trek.assigned_staff_id = staff.id

    db.session.commit()

    return jsonify({
        "message": "Staff assigned successfully"
    }), 200



@app.route("/staff/treks", methods=["GET"])
@jwt_required()
def staff_treks():

    if current_user.role != "staff":
        return jsonify({
            "message": "Access denied"
        }), 403

    treks = Trek.query.filter_by(
        assigned_staff_id=current_user.id
    ).all()

    result = []

    for trek in treks:
        result.append({
            "id": trek.id,
            "trek_name": trek.trek_name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "available_slots": trek.available_slots,
            "status": trek.status
        })

    return jsonify(result), 200

@app.route("/staff/trek/<int:trek_id>/status", methods=["PUT"])
@jwt_required()
def update_trek_status(trek_id):

    # Only staff can update trek status
    if current_user.role != "staff":
        return jsonify({
            "message": "Access denied"
        }), 403

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "message": "Trek not found"
        }), 404

    # Staff can update only their assigned trek
    if trek.assigned_staff_id != current_user.id:
        return jsonify({
            "message": "You are not assigned to this trek"
        }), 403

    data = request.get_json()

    status = data.get("status")

    allowed_status = [
        "Pending",
        "Approved",
        "Open",
        "Closed",
        "Completed"
    ]

    if status not in allowed_status:
        return jsonify({
            "message": "Invalid status"
        }), 400

    trek.status = status

    db.session.commit()

    return jsonify({
        "message": "Trek status updated successfully",
        "trek_id": trek.id,
        "new_status": trek.status
    }), 200

@app.route("/treks", methods=["GET"])
@jwt_required()
def get_open_treks():

    treks = Trek.query.filter_by(
        status="Open"
    ).all()

    result = []

    for trek in treks:
        result.append({
            "id": trek.id,
            "trek_name": trek.trek_name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "available_slots": trek.available_slots,
            "start_date": str(trek.start_date),
            "end_date": str(trek.end_date),
            "status": trek.status
        })

    return jsonify(result), 200

@app.route("/bookings", methods=["POST"])
@jwt_required()
def book_trek():

    if current_user.role != "user":
        return jsonify({
            "message": "Only users can book treks"
        }), 403

    data = request.get_json()

    trek_id = data.get("trek_id")

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "message": "Trek not found"
        }), 404

    if trek.status != "Open":
        return jsonify({
            "message": "Trek is not open for booking"
        }), 400

    if trek.available_slots <= 0:
        return jsonify({
            "message": "No slots available"
        }), 400

    existing_booking = Booking.query.filter_by(
        user_id=current_user.id,
        trek_id=trek_id
    ).first()

    if existing_booking:
        return jsonify({
            "message": "You have already booked this trek"
        }), 400

    booking = Booking(
        user_id=current_user.id,
        trek_id=trek_id,
        status="Booked"
    )

    trek.available_slots -= 1

    db.session.add(booking)
    db.session.commit()

    return jsonify({
        "message": "Trek booked successfully"
    }), 201

@app.route("/my-bookings", methods=["GET"])
@jwt_required()
def my_bookings():

    if current_user.role != "user":
        return jsonify({
            "message": "Access denied"
        }), 403

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).all()

    result = []

    for booking in bookings:
        result.append({
            "booking_id": booking.id,
            "trek_name": booking.trek.trek_name,
            "location": booking.trek.location,
            "booking_date": booking.booking_date,
            "status": booking.status
        })

    return jsonify(result), 200

@app.route("/admin/bookings", methods=["GET"])
@jwt_required()
def get_all_bookings():

    if current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    bookings = Booking.query.all()

    result = []

    for booking in bookings:
        result.append({
            "booking_id": booking.id,
            "username": booking.user.username,
            "trek_name": booking.trek.trek_name,
            "status": booking.status
        })

    return jsonify(result), 200

@app.route("/search/treks", methods=["GET"])
@jwt_required()
def search_treks():

    keyword = request.args.get("q")

    treks = Trek.query.filter(
        Trek.trek_name.ilike(f"%{keyword}%")
    ).all()

    result = []

    for trek in treks:
        result.append({
            "id": trek.id,
            "trek_name": trek.trek_name,
            "location": trek.location,
            "status": trek.status
        })

    return jsonify(result), 200

@app.route("/search/users", methods=["GET"])
@jwt_required()
def search_users():

    if current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    keyword = request.args.get("q")

    users = User.query.filter(
        User.username.ilike(f"%{keyword}%")
    ).all()

    result = []

    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })

    return jsonify(result), 200

@app.route("/search/staff", methods=["GET"])
@jwt_required()
def search_staff():

    if current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    keyword = request.args.get("q")

    staffs = User.query.filter(
        User.role == "staff",
        User.username.ilike(f"%{keyword}%")
    ).all()

    result = []

    for staff in staffs:
        result.append({
            "id": staff.id,
            "username": staff.username,
            "email": staff.email
        })

    return jsonify(result), 200


@app.route("/admin/deactivate-user/<int:user_id>", methods=["PUT"])
@jwt_required()
def deactivate_user(user_id):

    if current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    user.active = False

    db.session.commit()

    return jsonify({
        "message": "User deactivated successfully"
    }), 200

@app.route("/admin/deactivate-staff/<int:staff_id>", methods=["PUT"])
@jwt_required()
def deactivate_staff(staff_id):

    if current_user.role != "admin":
        return jsonify({
            "message": "Access denied"
        }), 403

    staff = User.query.filter_by(
        id=staff_id,
        role="staff"
    ).first()

    if not staff:
        return jsonify({
            "message": "Staff not found"
        }), 404

    staff.active = False

    db.session.commit()

    return jsonify({
        "message": "Staff deactivated successfully"
    }), 200

@app.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")

    if username:
        current_user.username = username

    if email:
        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user and existing_user.id != current_user.id:
            return jsonify({
                "message": "Email already exists"
            }), 409

        current_user.email = email

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully",
        "username": current_user.username,
        "email": current_user.email
    }), 200

@app.route("/staff/trek/<int:trek_id>/participants", methods=["GET"])
@jwt_required()
def view_participants(trek_id):

    if current_user.role != "staff":
        return jsonify({
            "message": "Access denied"
        }), 403

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "message": "Trek not found"
        }), 404

    if trek.assigned_staff_id != current_user.id:
        return jsonify({
            "message": "You are not assigned to this trek"
        }), 403

    bookings = Booking.query.filter_by(
        trek_id=trek_id
    ).all()

    result = []

    for booking in bookings:
        result.append({
            "user_id": booking.user.id,
            "username": booking.user.username,
            "email": booking.user.email,
            "booking_status": booking.status
        })

    return jsonify(result), 200
