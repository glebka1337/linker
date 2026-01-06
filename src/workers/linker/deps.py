# src/workers/linker/deps.py
from dataclasses import dataclass
import logging
from src.core.resources import Resources
from src.interfaces.note_repo_interface import NoteRepo
from src.interfaces.vector_repo_interface import NoteVectorRepo
from src.models.note import Note as NoteDoc
from src.repos.mongo_repo import MongoRepo
from src.repos.vector_repo import QdrantVectorRepo

logger = logging.getLogger(__name__)

@dataclass
class LinkerDeps:
    note_repo: NoteRepo
    vector_repo: NoteVectorRepo
    
async def assemble_linker(
    resources: Resources
) -> LinkerDeps:
    
    logger.info(f"Assembling all dependencies for linker worker")
    
    note_repo = MongoRepo(
        NoteDoc
    )
    
    vector_repo = QdrantVectorRepo(
        client=resources.qdrant_client
    )
    
    return LinkerDeps(
        note_repo=note_repo,
        vector_repo=vector_repo
    )