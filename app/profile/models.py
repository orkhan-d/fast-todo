from datetime import date
from app.db import Base, intpk, Mapped, mapped_column

class Profile(Base):
    __tablename__ = 'profiles'
    
    user_id: Mapped[intpk]

    address: Mapped[str | None] = mapped_column()
    balance: Mapped[int | None] = mapped_column()
    
    card_number: Mapped[str | None] = mapped_column()
    card_date: Mapped[date | None] = mapped_column()
    card_secret: Mapped[int | None] = mapped_column()