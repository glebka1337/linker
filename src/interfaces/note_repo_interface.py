from typing import List, Protocol, Optional
from src.core.entities.note import NoteEntity
from src.schemas.note import NoteTitleProjection

class NoteRepo(Protocol):
    """
    Protocol defining the interface for note repository operations.
    Ensures that all implementations provide multi-tenant support 
    via owner_uuid filtering.
    """
    
    async def get_by_uuid(
        self, note_uuid: str, owner_uuid: str
    ) -> Optional[NoteEntity]:
        """
        Retrieves a specific note by its UUID and owner ID.

        Args:
            note_uuid (str): The unique identifier of the note.
            owner_uuid (str): The identifier of the user who owns the note.

        Returns:
            Optional[NoteEntity]: The note entity if found and owned by the user, else None.
        """
        ...
    
    async def get_by_uuids(
        self, uuids: List[str], owner_uuid: str, lim: Optional[int] = None
    ) -> List[NoteEntity]:
        """
        Retrieves a list of notes matching the provided UUIDs and owner ID.

        Args:
            uuids (List[str]): List of note UUIDs to retrieve.
            owner_uuid (str): The identifier of the user who owns the notes.
            lim (Optional[int]): Maximum number of notes to return.

        Returns:
            List[NoteEntity]: A list of note entities owned by the user.
        """
        ...
    
    async def get_titles_by_uuids(
        self,
        uuids: List[str],
        owner_uuid: str
    ) -> List[NoteTitleProjection]:
        """
        Retrieves note projections (title and uuid) for a list of UUIDs.
        Used for lightweight link resolution.

        Args:
            uuids (List[str]): List of note UUIDs to search for.
            owner_uuid (str): The identifier of the user who owns the notes.

        Returns:
            List[NoteTitleProjection]: A list of projections for owned notes.
        """
        ...
    
    async def get_all(
        self,
        owner_uuid: str
    ) -> List[NoteEntity]:
        """
        Retrieves all notes belonging to a specific user.

        Args:
            owner_uuid (str): The identifier of the user.

        Returns:
            List[NoteEntity]: A list of all notes owned by the user.
        """
        ...
    
    async def create(
        self, note_data: NoteEntity
    ) -> NoteEntity:
        """
        Persists a new note entity in the database.
        The owner_uuid must be pre-set within the note_data.

        Args:
            note_data (NoteEntity): The note entity to be created.

        Returns:
            NoteEntity: The created note entity as stored in the database.
        """
        ...
    
    async def update(
        self, note: NoteEntity, owner_uuid: str
    ) -> Optional[NoteEntity]: 
        """
        Updates an existing note after verifying ownership.

        Args:
            note (NoteEntity): The note entity with updated data.
            owner_uuid (str): The identifier of the user attempting the update.

        Returns:
            Optional[NoteEntity]: The updated note entity, or None if the note 
                                 does not exist or ownership is not verified.
        """
        ...
    
    async def delete(
        self,
        note_uuid: str,
        owner_uuid: str
    ) -> bool:
        """
        Deletes a note by its UUID after verifying ownership.

        Args:
            note_uuid (str): The UUID of the note to delete.
            owner_uuid (str): The identifier of the user attempting the deletion.

        Returns:
            bool: True if the note was successfully deleted, False otherwise.
        """
        ...
    
    async def remove_related_links(
        self,
        target_uuid: str,
        owner_uuid: str
    ) -> None:
        """
        Removes a specific note UUID from the related_notes lists across 
        all notes owned by the user. Used for maintaining link consistency.

        Args:
            target_uuid (str): The note UUID to be removed from references.
            owner_uuid (str): The identifier of the user who owns the notes.
        """
        ...