# imports the supplied names into the Person table in the sqlite DB supplied in the config
import peewee
from webapp.models import Person

names = """DOE, JOHN
BESS, CHRISTOPHER
DOE, JANE"""

# iterate names to import
for name in names.split('\n'):
    # normalize the name
    parts = name.split(',')
    name = '%s %s' % (parts[1].strip().title(), parts[0].strip().title())
    # prevent duplicates
    if Person.filter(name=name).exists():
        continue
    person = Person(name=name)
    person.save()
    pass
    
print 'Count: %s' % Person.select().count()
    