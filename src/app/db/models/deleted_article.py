from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from src.app.db.base import Base


class DeletedArticle(Base):
    __tablename__ = "deleted_articles"

    id = Column(Integer, primary_key=True, index=True)
    original_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)
    image_url = Column(String(1024), nullable=True)
    category_id = Column(Integer, nullable=False)
    author_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
