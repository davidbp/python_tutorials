from docarray import Document
from pprint import pprint

doc_schema = {
    'classes': [
        {
            'class': 'JinaDocv',
            'properties': [
                {'dataType': ['blob'], 'name': '_serialized'},
            ],
        }
    ]
}

import weaviate

client = weaviate.Client('http://localhost:8080')

class_exists = False
for c in client.schema.get()['classes']:
    if 'JinaDocv' in c['class']:
        print('\nJinaDocv found\n')
        pprint(c)
        class_exists = True

if class_exists == False:
    print('\nCreating schema with client.schema.create(doc_schema)\n')
    client.schema.create(doc_schema)

d = Document(embedding=[1, 2, 3])
did = client.data_object.create({'_serialized': d.to_base64()},
                                 class_name='JinaDocv',
                                 vector=d.embedding)

print(Document.from_base64(client.data_object.get_by_id(did)['properties']['_serialized']))
