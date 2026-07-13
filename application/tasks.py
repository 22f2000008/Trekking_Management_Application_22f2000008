import csv
import os

from flask_mail import Message

from app import celery, app, mail
from flask_mail import Message
from application.models import Booking, User , Trek
from application.database import db


# Export Booking History (CSV)
 
@celery.task
def export_booking_history(user_id):

    with app.app_context():

        # Get user
        user = User.query.get(user_id)

        # Get bookings
        bookings = Booking.query.filter_by(user_id=user_id).all()

        # Create exports folder
        folder = "exports"
        os.makedirs(folder, exist_ok=True)

        filename = f"{folder}/booking_history_{user_id}.csv"

        # Create CSV
        with open(filename, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Booking ID",
                "Trek",
                "Location",
                "Booking Date",
                "Status"
            ])

            for booking in bookings:

                writer.writerow([
                    booking.id,
                    booking.trek.trek_name,
                    booking.trek.location,
                    booking.booking_date,
                    booking.status
                ])

        # Create email
        msg = Message(
            subject="Your Booking History",
            recipients=[user.email]
        )

        msg.body = f"""
Hello {user.username},

Your booking history has been exported successfully.

The CSV file is attached with this email.

Regards,
Trekking Management Application
"""

        # Attach CSV
        with open(filename, "rb") as f:
            msg.attach(
                filename="booking_history.csv",
                content_type="text/csv",
                data=f.read()
            )

        # Send email
        mail.send(msg)

        return "CSV exported and emailed successfully"


# Daily Reminder Email
 
@celery.task
def daily_reminder():

    with app.app_context():

        bookings = Booking.query.filter_by(status="Booked").all()

        for booking in bookings:

            msg = Message(
                subject="Upcoming Trek Reminder",
                recipients=[booking.user.email]
            )

            msg.body = f"""
Hello {booking.user.username},

This is a reminder for your upcoming trek.

Trek Name : {booking.trek.trek_name}
Location  : {booking.trek.location}
Start Date: {booking.trek.start_date}
End Date  : {booking.trek.end_date}

Have a safe and enjoyable trek!

Regards,
Trekking Management Team
"""

            mail.send(msg)

    return "Reminder emails sent successfully"


# Monthly HTML Report
 
@celery.task
def monthly_report():

    with app.app_context():

        # Total treks
        total_treks = Trek.query.count()

        # Total bookings
        total_bookings = Booking.query.count()

        # Users who actually participated
        total_users = (
            db.session.query(Booking.user_id)
            .distinct()
            .count()
        )

        # Most popular trek
        popular_trek = (
            db.session.query(
                Trek.trek_name,
                db.func.count(Booking.id).label("count")
            )
            .join(Booking)
            .group_by(Trek.id)
            .order_by(db.desc("count"))
            .first()
        )

        popular = popular_trek.trek_name if popular_trek else "No bookings"

         
        admin = User.query.filter_by(role="admin").first()

        if not admin:
            return "Admin not found"

        # HTML report
        html = f"""
        <h2>Monthly Trekking Activity Report</h2>

        <table border="1" cellpadding="8" cellspacing="0">
            <tr>
                <th>Total Treks Conducted</th>
                <td>{total_treks}</td>
            </tr>

            <tr>
                <th>Total Users Participated</th>
                <td>{total_users}</td>
            </tr>

            <tr>
                <th>Total Bookings</th>
                <td>{total_bookings}</td>
            </tr>

            <tr>
                <th>Most Popular Trek</th>
                <td>{popular}</td>
            </tr>
        </table>

        <br><br>

        Regards,<br>
        <b>Trekking Management Application</b>
        """

        msg = Message(
            subject="Monthly Trekking Activity Report",
            recipients=[admin.email],
            html=html
        )

        mail.send(msg)

    return "Monthly report sent successfully"