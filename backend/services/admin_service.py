from datetime import datetime
from models.user import User
from models.resume_history import ResumeHistory, SearchLog


def get_all_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return [u.to_dict() for u in users]


def get_user_resumes(user_id):
    rows = ResumeHistory.query.filter_by(user_id=user_id)\
               .order_by(ResumeHistory.created_at.desc()).all()
    return [r.to_dict() for r in rows]


def get_activity(from_date_str=None, to_date_str=None):
    q = SearchLog.query.join(User, SearchLog.user_id == User.id)

    if from_date_str:
        try:
            from_dt = datetime.fromisoformat(from_date_str)
            q = q.filter(SearchLog.timestamp >= from_dt)
        except ValueError:
            pass

    if to_date_str:
        try:
            to_dt = datetime.fromisoformat(to_date_str)
            q = q.filter(SearchLog.timestamp <= to_dt)
        except ValueError:
            pass

    rows = q.order_by(SearchLog.timestamp.desc()).all()
    result = []
    for row in rows:
        d = row.to_dict()
        d["user_name"]  = row.user.name
        d["user_email"] = row.user.email
        result.append(d)
    return result