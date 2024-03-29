from app.db import Base, intpk, Mapped, mapped_column, BIGINT, ForeignKey

class Todo(Base):
    __tablename__ = 'todos'
    
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id_'), type_=BIGINT)
    text: Mapped[str] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id_'))
    done: Mapped[bool] = mapped_column(default=False)