import json
import sys

if len(sys.argv) > 2:
    print("ERROR: 1 argument requiered, number of hsk to be transformed")
    exit()
if sys.argv[1] not in ['1', '2', '3', '4', '5', '6']:
    print("ERROR: argument must be a number between 1 and 6 inclusive")
    exit()
hsk = int(sys.argv[1])

print('DEBUG: Reading json file')
with open('hsk-level-{}.json'.format(hsk), 'r', encoding="utf8") as f:
    vocabulary = json.load(f)

print('DEBUG: Starting transform data')
transformed_json = []
for word in vocabulary:
    new_dict = {}
    new_dict['model'] = "chinesetest.Word"
    new_dict['pk'] = word['id'] - 1
    new_dict['fields'] = {}
    new_dict['fields']['hanzi'] = word['hanzi']
    new_dict['fields']['pinyin'] = word['pinyin']
    new_dict['fields']['hsk'] = hsk
    new_dict['fields']['meaning'] = ', '.join(word['translations'])

    transformed_json.append(new_dict)

print('DEBUG: Dumping json file')
with open('hsk{}_transformed.json'.format(hsk), 'w', encoding='utf8') as transformed_json_file:
    json.dump(transformed_json , transformed_json_file, indent=4, ensure_ascii=False)

print('Process ended correctly')