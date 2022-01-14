from docarray import Document
from typing import Union
import numpy as np
import uuid


def write_to_weaviate(client, doc: Document, class_name:str='Document'):

    client.data_object.create({'serialized_doc': doc.to_base64()},
                               class_name=class_name,
                               vector=doc.embedding,
                               uuid = str(uuid.UUID(doc.id)))


def get_all_docs(client,
                 doc_class='Document',
                 attribute_container='serialized_doc'):
    
    s_docs = client.query.get('Document', ['serialized_doc']).do()
    sdocs = [s['serialized_doc'] for s in s_docs['data']['Get']['Document']]
    return [Document.from_base64(sdoc) for sdoc in sdocs ]


def get_doc_by_id(client, doc_id):

    result_dict = client.data_object.get_by_id(doc_id)
    
    if result_dict is None:
        return None
    else:
        serialized_doc = result_dict['properties']['serialized_doc']

    return Document.from_base64(serialized_doc)


def search_near_docs(client, query_doc):
    
    embedding = query_doc.embedding

    if isinstance(embedding, np.ndarray):
        query_embedding = {'vector': embedding.tolist()}
    if isinstance(embedding, list):
        query_embedding = {'vector': embedding}
            
    dict_results = client.query.get('Document', ['_additional {certainty}','_additional {id}']).with_near_vector(query_embedding).do()
    weav_doc_ids = [r['_additional']['id'] for r in dict_results['data']['Get']['Document']]

    near_docs = []
    for doc_id in weav_doc_ids:
        near_docs.append(get_doc_by_id(client, doc_id))

    return near_docs


def delete_given_id(client, doc_id):
    client.data_object.delete(str(uuid.UUID(doc_id)))

def update_doc_given_id(client, doc):
    """
    This would be similar to `da[id] = new_doc`
    """

    client.data_object.replace(
        data_object = {'serialized_doc': doc.to_base64()},
        vector=[0,0,0], # if this line is commented get error
        class_name = 'Document',
        uuid = doc.id)





