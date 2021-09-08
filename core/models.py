from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "list_of_users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    list_of_decks = relationship("Deck", back_populates="user", passive_deletes=True)


# na razie flashcard - - jeden - - deck
class Deck(Base):
    __tablename__ = "list_of_decks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    tag = Column(String)
    public = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("list_of_users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="list_of_decks")
    list_of_flashcards = relationship("Flashcard", back_populates="deck", passive_deletes=True)


class Flashcard(Base):
    __tablename__ = "list_of_flashcards"

    id = Column(Integer, primary_key=True, index=True)
    averse = Column(String)
    reverse = Column(String)
    tip = Column(String)
    deck_id = Column(Integer, ForeignKey("list_of_decks.id", ondelete="CASCADE"))
    deck = relationship("Deck", back_populates="list_of_flashcards")
    level_id = Column(Integer, ForeignKey("list_of_levels.id"))
    level = relationship("Level", back_populates="list_of_flashcards")


class Level(Base):
    __tablename__ = "list_of_levels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    repeat_frequency = Column(Integer)
    list_of_flashcards = relationship("Flashcard", back_populates="level", passive_deletes=True)
