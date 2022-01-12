from docarray import Document

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

# only do this one-time, otherwise an error schema exist
# client.schema.create(doc_schema)

d = Document(embedding=[1, 2, 3])

did = client.data_object.create({'_serialized': d.to_base64()},
                                class_name='JinaDocv',
                                vector=d.embedding)

print(Document.from_base64(client.data_object.get_by_id(did)['properties']['_serialized']))
