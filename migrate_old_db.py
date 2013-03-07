# Migrates the sqlite db to the new mongodb database (sqlite -> mongodb)
# Created by: C. Bess
# All logs will be ignored, so users must checkin/out the inventory once migration is complete

from webapp.models import Person, User, InventoryItem, InventoryGroup
from peewee import * # >= 2.x

## Settings

db_path = 'webapp.db'

## Models

sqlite_db = SqliteDatabase(db_path, **{})

# generated using pwiz.py

class LegacyBaseModel(Model):
    class Meta:
        database = sqlite_db

class LegacyInventoryGroup(LegacyBaseModel):
    name = CharField()

    class Meta:
        db_table = 'inventorygroup'

class LegacyInventoryItem(LegacyBaseModel):
    comment = CharField()
    date_added = DateTimeField()
    date_updated = DateTimeField()
    group = ForeignKeyField(db_column='group_id', rel_model=LegacyInventoryGroup)
    identifier = CharField()
    name = CharField()
    status = IntegerField()

    class Meta:
        db_table = 'inventoryitem'

class LegacyPerson(LegacyBaseModel):
    name = CharField()

    class Meta:
        db_table = 'person'

class LegacyUser(LegacyBaseModel):
    email = CharField()
    is_admin = IntegerField()
    name = CharField()
    password = CharField()

    class Meta:
        db_table = 'user'


sqlite_db.connect()

## Ad-hoc migration

# move all persons
for person in LegacyPerson.select():
    if Person.objects(name=person.name).count():
        continue
    Person(name=person.name).save()
    print 'Migrated Person: '+person.name

# move all users
for user in LegacyUser.select():
    if User.objects(name=user.name).count():
        continue
    # transfer user data
    User(
        name=user.name,
        email=user.email,
        password=user.password,
        is_admin=bool(user.is_admin)
    ).save()
    print 'Migrated User: '+user.name
    
# move groups
for group in LegacyInventoryGroup.select():
    if InventoryGroup.objects(name=group.name).count():
        continue
    InventoryGroup(
        name=group.name,
        identifier=str(group.id)
    ).save()
    print 'Migrated Group: '+group.name
    
# move items
for item in LegacyInventoryItem.select():
    if InventoryItem.objects(name=item.name).count():
        continue
    # get the group
    group = InventoryGroup.objects.get(name=item.group.name)
    # create item
    InventoryItem(
        group=group,
        name=item.name,
        identifier=item.identifier,
        comment=item.comment,
        date_added=item.date_added,
        date_updated=item.date_updated,
        status=int(item.status)
    ).save()
    print 'Migrated Inventory Item: '+item.name
    
