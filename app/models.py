from tortoise.models import Model
from tortoise import fields


class Job(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField()

    def __str__(self):
        return self.name


class Player(Model):
    id = fields.IntField(pk=True)
    nickname = fields.CharField(max_length=255)
    job = fields.ForeignKeyField(
        'models.Job', related_name='players')
    participants = fields.ManyToManyField(
        'models.Team', related_name='players', through='player_team')

    def __str__(self):
        return self.nickname


class Team(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name
