from database import db
from datetime import datetime

class EmailToken(db.Model):
    __tablename__ = "email_tokens"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    token      = db.Column(db.String(256), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ResumeHistory(db.Model):
    __tablename__ = "resume_history"

    id                  = db.Column(db.Integer, primary_key=True)
    user_id             = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    job_title           = db.Column(db.String(200))
    ats_score           = db.Column(db.Float)
    uploaded_file_path  = db.Column(db.String(400))
    optimised_file_path = db.Column(db.String(400))
    pdf_path            = db.Column(db.String(400))
    docx_path           = db.Column(db.String(400))
    created_at          = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":                  self.id,
            "job_title":           self.job_title,
            "ats_score":           self.ats_score,
            "uploaded_file_path":  self.uploaded_file_path,
            "optimised_file_path": self.optimised_file_path,
            "pdf_path":            self.pdf_path,
            "docx_path":           self.docx_path,
            "created_at":          self.created_at.isoformat(),
        }


class SearchLog(db.Model):
    __tablename__ = "search_logs"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    query_text = db.Column(db.Text)
    timestamp  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":         self.id,
            "user_id":    self.user_id,
            "query_text": self.query_text,
            "timestamp":  self.timestamp.isoformat(),
        }