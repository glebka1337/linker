from typing import Any
from beanie.operators import In
from src.models.note import Note, RelatedNote
import pytest
from motor.motor_asyncio import (
    AsyncIOMotorCollection
)
from bson import ObjectId

def _generate_notes()-> list[dict[str, Any]]:
    return [{'title': f'Title {i}', 'text': str(i), 'related': []} for i in range(10)]

@pytest.mark.asyncio
async def test_insert(
    test_collection: AsyncIOMotorCollection
):
    # create collectio
    
    result = await test_collection.insert_one(document={
        "title": "TestNote"
    })
    
    print(result.inserted_id)
    assert (result.inserted_id is None) != True

@pytest.mark.asyncio
async def test_search_embedded_docs(
    test_collection:AsyncIOMotorCollection
):
    # create documents 
    docs = _generate_notes()
    results = await test_collection.insert_many(docs)
    
    # insert doc that refer to documents
    doc_main = {
        'title': 'TestMain',
        'content': 'TestContent',
        'related_notes': [str(id_) for id_ in results.inserted_ids]
    }
    
    result = await test_collection.insert_one(document=doc_main)
    
    # update related docs
    
    await test_collection.update_many(
        filter={"_id": {"$in": results.inserted_ids} },
        update={
            "$addToSet": {"related": result.inserted_id}
        }
    )
    
    # check if they updated 
    
    docs_updated = await test_collection.find(filter={
        "_id": {"$in": results.inserted_ids}
    }).to_list(length=100)
    
    for d in docs_updated:
        assert ObjectId(result.inserted_id) in d["related"]
    
    
@pytest.mark.asyncio
async def test_note_model_insert(
    test_db
):
    note = Note(
        title="TestMainNote",
        text="Text"
    )
    
    await note.insert()
    
    # update note
    assert note.id is not None
    

@pytest.mark.asyncio
async def test_note_relations(
    test_db
):
    # create notes
    
    notes = await Note.insert_many(
        [
          Note(
              title=n.get("title", "Default Title"),
              text=n.get("text", "Default Text"),
          ) for n in _generate_notes()
        ]
    )
    
    # create one note
    note = Note(title="Test Title", text="Test Text", related_notes=[
        RelatedNote(
            note_id=str(id_),
            score= 0.8
        ) for id_ in notes.inserted_ids
    ])
    
    await note.insert()
    
    # update other notes, they are related now
    
    await Note.find(In(Note.id, notes.inserted_ids))\
            .update_many({
                "$addToSet": {
                    "related_notes": {
                        "note_id": str(note.id),
                        "score": 0.8,
                    }
                }
            })
            
    # check if ids are present in both notes and a main note
    
    notes_updated = await Note.find(In(Note.id, notes.inserted_ids)).to_list()
    for n in notes_updated:
        assert any(
            r.note_id == str(note.id) for r in n.related_notes
        )
    