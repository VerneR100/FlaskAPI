# models.py
from validate_email import validate_email
from json import dumps


class User:
    ID = 0

    def __init__(self, first_name, last_name, email, sport):
        self.id = self.ID
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.sport = sport
        self.contests = list()
        self.update_ID()

    @classmethod
    def update_ID(cls):
        cls.ID += 1

    def add_contest(self, id):
        self.contests.append(id)

    def data(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "contests": self.contests,
        }

    def response(self):
        return dumps(self.data())

    @staticmethod
    def is_valid_email(email):
        return validate_email(email)

    @staticmethod
    def leaderboard(users, types_of_sorting):
        pass


class Contest:
    ID = 0

    def __init__(self, name, sport, participants):
        self.id = self.ID
        self.name = name
        self.sport = sport
        self.status = "STARTED"
        self.participants = participants
        self.winner = None
        self.update_ID()

    @classmethod
    def update_ID(cls):
        cls.ID += 1

    def finish_contest(self, winner):
        self.status = "FINISHED"
        self.winner = winner

    def data(self):
        return {
            "id": self.id,
            "name": self.name,
            "sport": self.sport,
            "status": self.status,
            "participants": self.participants,
            "winner": self.winner,
        }

    def response(self):
        return dumps(self.data())
