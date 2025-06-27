from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String


class Task(SQLAlchemy().Model):
    tid: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column() 
    isComplete: Mapped[bool] = mapped_column(default=False)
    createdAt:Mapped[datetime] = mapped_column(default=datetime.now)
    
    def __repr__(self):
        return f"Task: {self.tid}"
