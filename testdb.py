from peewee import *

db = MySQLDatabase('campapas', user='xqqp2hmmrkwg', password='pscale_pw__g4UN3FQ0s-l3ONtGGiVp9hegkGjXyMuHgOa2XVMLEs',
                         host='oq762iss76uk.us-east-4.psdb.cloud', port=3306)

result = db.connect()

print(result)