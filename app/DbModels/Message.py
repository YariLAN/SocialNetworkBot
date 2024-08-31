from sqlite3 import Date


class MessageMapper(object):
    @staticmethod
    def toMap(sender_id, recipient_id, text):
        sen_id = int(sender_id)
        rec_id = int(recipient_id)
        return Message(sen_id, rec_id, text, Date.today())


class Message:
    __tableName__ = "messages"

    def __init__(self, sender_id, recipient_id, text, date_message):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.text = text
        self.date_message = date_message
