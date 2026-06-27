import secrets
from flask import current_app, url_for
from flask_mail import Message
from database import db, mail
from models.resume_history import EmailToken


def send_verification_email(user):
    token_str = secrets.token_urlsafe(32)
    record = EmailToken(user_id=user.id, token=token_str)
    db.session.add(record)
    db.session.commit()

    verify_url = f"http://localhost:5500/verify.html?token={token_str}"

    msg = Message(
        subject="Verify your ResumeAI account",
        recipients=[user.email],
        html=f"""
        <div style="font-family:sans-serif;max-width:520px;margin:auto;padding:32px">
          <h2 style="color:#4f46e5">Welcome to ResumeAI, {user.name}!</h2>
          <p style="color:#444;line-height:1.6">
            Click the button below to verify your email address.
            This link expires in 24 hours.
          </p>
          <a href="{verify_url}"
             style="display:inline-block;margin:24px 0;padding:12px 28px;
                    background:#4f46e5;color:#fff;border-radius:8px;
                    text-decoration:none;font-weight:600">
            Verify Email
          </a>
          <p style="color:#888;font-size:13px">
            If you didn't create an account, ignore this email.
          </p>
        </div>
        """,
    )
    mail.send(msg)