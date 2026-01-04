import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_note(
    http_client: AsyncClient
):
    note = {
        "title": "test",
        "text": "test"
    }
    
    response = await http_client.post(url='notes/', json=note)
    
    assert response.status_code == 201
    
@pytest.mark.asyncio
async def test_get_all_notes(
    http_client: AsyncClient
):
    N = 10
    
    notes = [
        {
            "title": f"title {i}",
            "text": f"text {i}"
        }
        for i in range(N)
    ]
    
    resps_codes = []
    for d in notes:
        r = await http_client.post(
            url='notes/',
            json=d
        )
        resps_codes.append(r.status_code)
        
    assert all([code == 201 for code in resps_codes]) == True
    
    # get all notes
    
    notes_response = await http_client.get(
        url='notes/'
    )
    
    notes_response = notes_response.json()
    
    assert len(notes_response) == N