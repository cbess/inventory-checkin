# Imports the supplied names into the Person table in the DB 
# supplied in the config
from webapp.models import Person

# CSV text
names = """DOE, JOHN
BESS, CHRISTOPHER
DOE, JANE"""

import_count = 0
skip_count = 0
# iterate names to import
for name in names.split('\n'):
    # normalize the name
    parts = name.split(',')
    name = '%s %s' % (parts[1].strip().title(), parts[0].strip().title())
    # prevent duplicates
    if Person.objects(name=name).count():
        skip_count += 1
        continue
    person = Person(name=name)
    person.save()
    import_count += 1
    
print 'Imported %d persons, %d skipped. Total: %d' % \
    (import_count, skip_count, Person.objects.count())
    