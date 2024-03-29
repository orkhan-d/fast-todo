from app.db import Base, intpk, Mapped, mapped_column, BIGINT, ForeignKey

class Category(Base):
    __tablename__ = 'categories'
    
    id_: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id_'), type_=BIGINT)
    name: Mapped[str] = mapped_column()