import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, Text, DateTime, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class BaseMemory(Base):
    __tablename__ = "base_memories"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<BaseMemory(id={self.id}, updated_at={self.updated_at})>"

class MemoryPyramid(Base):
    __tablename__ = "memory_pyramids"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    base_id = Column(Integer, ForeignKey("base_memories.id"), nullable=False)
    theme = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    base_memory = relationship("BaseMemory", backref="pyramids")

    def __repr__(self):
        return f"<MemoryPyramid(id={self.id}, theme={self.theme})>"

class PyramidLevel(Base):
    __tablename__ = "pyramid_levels"

    id = Column(Integer, primary_key=True)
    pyramid_id = Column(UUID(as_uuid=True), ForeignKey("memory_pyramids.id"), nullable=False)
    level = Column(Integer, nullable=False)  # 0 to 5
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("pyramid_id", "level", name="_pyramid_level_uc"),)

    pyramid = relationship("MemoryPyramid", backref="levels")

    def __repr__(self):
        return f"<PyramidLevel(pyramid_id={self.pyramid_id}, level={self.level})>"
