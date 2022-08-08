from sqlalchemy import Column, String, Numeric
from bot.helpers.sql_helper import SESSION, BASE


class ParentID(BASE):
    __tablename__ = "ParentID"
    chat_id = Column(Numeric, primary_key=True)
    parent_id = Column(String)
    parent_name = Column(String)


    def __init__(self, chat_id, parent_id, parent_name):
        self.chat_id = chat_id
        self.parent_id = parent_id
        self.parent_name = parent_name
        

ParentID.__table__.create(checkfirst=True)

def search_parent(chat_id):
    try:
        return SESSION.query(ParentID).filter(ParentID.chat_id == chat_id).one().parent_id
    except:
        return 'root'
    finally:
        SESSION.close()

def search_pname(chat_id):
    try:
        return SESSION.query(ParentID).filter(ParentID.chat_id == chat_id).one().parent_name
    except:
        return 'root'
    finally:
        SESSION.close()


def _set(chat_id, parent_id, parent_name):
    adder = SESSION.query(ParentID).get(chat_id)
    print(adder)
    if adder:
        adder.parent_id = parent_id
        adder.parent_name = parent_name
    else:
        adder = ParentID(
            chat_id,
            parent_id,
            parent_name
        )
    SESSION.add(adder)
    SESSION.commit()


def _clear(chat_id):
    rem = SESSION.query(ParentID).get(chat_id)
    if rem:
        SESSION.delete(rem)
        SESSION.commit()