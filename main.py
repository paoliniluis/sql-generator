import random, os, argparse, pgzip, yaml

from datetime import datetime
from mimesis import Generic
from mimesis.locales import Locale

parser = argparse.ArgumentParser()
parser.add_argument("config")
parser.add_argument("target")
parser.add_argument("n_of_rows")
args = parser.parse_args()
generic = Generic(locale=Locale.EN)

def createTable(table_name:str, fields:str) -> str:
    return f"CREATE TABLE IF NOT EXISTS {table_name} ({fields});"

def insertValues(table_name:str, fields:str) -> str:
    return f"INSERT INTO {table_name} ({fields}) VALUES"

def generateValueList (itemList: list) -> str:
    iterator = map(lambda item: str(generateValue(item)), itemList)
    return '(' + ','.join(iterator) + '),'
    
def fieldNamesOnly (fields: list) -> str:
    return ','.join(generateOnlyFieldNames(fields))

def fieldNamesWithTypes (fields: list) -> str:
    return ','.join(fields)

def generateOnlyFieldNames (fields:list) -> map:
    return map (getFieldName, fields)

def getFieldName (item) -> list:
    return item[:item.find(' ')]

def generateValue(fieldType:str) -> any:
    if fieldType == 'boolean':
        return f"{generic.development.boolean()}"
    if fieldType == 'varchar':
        return f"'{generic.food.fruit().replace(chr(39),'').replace(chr(44),'').replace(chr(34),'')}'"
    if fieldType == 'text':
        return f"'{generic.text.text(3).replace(chr(39),'').replace(chr(44),'').replace(chr(34),'')}'"
    if fieldType == 'date':
        return f"'{generic.datetime.date()}'"
    if fieldType == 'timestamp':
        return f"'{generic.datetime.datetime()}'"
    if fieldType == 'integer':
        return random.randint(-2147483648,2147483647)
    if fieldType == 'decimal':
        return random.random()*100
    if fieldType == 'inet':
        return f"'{generic.internet.ip_v4()}'"
    if fieldType == 'macaddr':
        return f"'{generic.internet.mac_address()}'"
    if fieldType == None:
        return ""

def main():
    config = args.config[args.config.find("=")+1:len(args.config)]
    target = args.target[args.target.find("=")+1:len(args.target)]
    n_of_rows = args.n_of_rows[args.n_of_rows.find("=")+1:len(args.n_of_rows)]

    start = datetime.now()
    print(start, f'getting config from {config}')
    print(start, f'dumping SQL to {target}finalSQL.sql.gz')
    print(start, f'generating {n_of_rows} rows')
    
    if os.path.isfile(f'{target}finalSQL.sql.gz'):
        os.remove(f'{target}finalSQL.sql.gz')
    with open(config, "r") as stream:
        try:
            definition = yaml.safe_load(stream)
            for table in definition['tables']:
                fields = []
                items = []
                for item in definition['tables'][table]:
                    for i in range(definition['tables'][table][item]):
                        fields.append(f"{table}_{item}{i} {item}")
                        items.append(item)
                
                with pgzip.open(f"{target}finalSQL.sql.gz", 'at') as file:
                    file.write(createTable(table, fieldNamesWithTypes(fields)) + '\n')
                    file.write(insertValues(table, fieldNamesOnly(fields)) + '\n')
                    for i in range(int(n_of_rows)):
                        if i == int(n_of_rows) - 1:
                            file.write(generateValueList(items).replace('),',');') + '\n')
                        else:
                            file.write(generateValueList(items) + '\n')
        except yaml.YAMLError as exc:
            print(exc)
    
    finish = datetime.now()
    difference = finish - start
    print(finish, f'finished creating {n_of_rows} rows at {finish}, took {difference.total_seconds()} seconds')
    
main()