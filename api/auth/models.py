from api.db import Base, intpk, Mapped, mapped_column

class User(Base):
    __tablename__ = 'users'
    
    id_: Mapped[intpk]
    name: Mapped[str | None] = mapped_column()
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    access_token: Mapped[str | None] = mapped_column()