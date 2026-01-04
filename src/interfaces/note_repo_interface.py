# src/interfaces/note_repo_interface.py
from typing import List, Protocol

from src.core.entities.note import NoteEntity

class NoteRepo(Protocol):
    
    async def get_by_uuid(
        self, note_uuid: str
    ) -> NoteEntity | None:
        """
        Method to get Note by uuid

        Args:
            
            note_uuid (str): note UUID

        Returns:
        
            NoteEntity | None: if note exists then 'Note', else None
            DOES NOT raise any exceptions
        """
        ...
    
    async def get_by_uuids(
        self, uuids: List[str], lim: int | None
    ) -> List[NoteEntity]:
        """
        Returns a list of notes with uuids provided

        Args:
        
            uuids (List[str]): UUIDs of notes
            lim (int): limit to retrieve. If not provided, will return all related

        Returns:
        
            List[NoteEntity]: Notes itself
        """
        ...
    
    async def get_all(
        self,
        # user_id
    ) -> List[NoteEntity]:
        """
        Retrieves all notes from the database.

        Args:
        
            # user_id (str): user ID of the notes to retrieve

        Returns:
        
            List[NoteEntity]: A list of all the notes in the database.
        """
        ...
    
    async def create(
        self, note_data: NoteEntity
    ) -> NoteEntity:
        
        """
        Creates a new note in the database.

        Args:
            note_data (NoteEntity): the note to be created

        Returns:
            NoteEntity: the newly created note
        """
        ...
    
    async def update(
        self, note: NoteEntity
    ) -> NoteEntity | None: 
        """
        Updates a note in the database.

        Args:
            note (NoteEntity): the note to be updated

        Returns:
        
            NoteEntity | None: the updated note or none if note with uuid was not found
            
        """
        ...
    
    