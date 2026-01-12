import logging
from src.interfaces.note_repo_interface import NoteRepo
from src.schemas.note import NoteRead, RelatedNoteResponse

logger = logging.getLogger(__name__)

class GetNoteUseCase:
    def __init__(
        self,
        repo: NoteRepo,
    ):
        self.repo = repo
    
    async def execute(
        self, note_uuid: str, owner_uuid: str
    ) -> NoteRead | None: 
        logger.info(f"{self.__class__.__name__} searching for a note: {note_uuid} ...")
        main_note = await self.repo.get_by_uuid(note_uuid, owner_uuid)
        
        if not main_note:
            return None
        
        # now we need dynamically get related note titles
        
        note_uuids = [n.note_uuid for n in main_note.related_notes]
        
        enriched_notes = [] # list for notes with enriched titles
        
        if note_uuids:
            
            logger.info(f'Fetching related note titles')

            related_notes = await self.repo.get_titles_by_uuids(note_uuids, owner_uuid=owner_uuid) # note(uuid, title)
            
            # to avoid double "for"
            doc_map = {n.uuid: n.title for n in related_notes}
            
            for rel in main_note.related_notes:
                note_title = doc_map.get(rel.note_uuid)
                
                if note_title:
                    enriched_notes.append(
                        RelatedNoteResponse(
                            title=note_title,
                            score=rel.score,
                            uuid=rel.note_uuid
                        )
                    )
        return NoteRead(
            uuid=main_note.uuid,
            title=main_note.title,
            text=main_note.text,
            created_at=main_note.created_at,
            related_notes=enriched_notes
        )