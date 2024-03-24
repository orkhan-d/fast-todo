from datetime import date
from app.db import Base, intpk, Mapped, mapped_column

class Profile(Base):
    __tablename__ = 'profiles'
    
    user_id: Mapped[intpk]
    
    name: Mapped[str | None] = mapped_column()
    surname: Mapped[str | None] = mapped_column()
    patronymic: Mapped[str | None] = mapped_column()
    phone: Mapped[str | None] = mapped_column()