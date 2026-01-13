#!/bin/bash

RAND_ID=$RANDOM
URL="http://localhost:8000"

EMAIL="test_${RAND_ID}@test.com"
USERNAME="TestUser_${RAND_ID}"
PASS="StrongPass123!"
NOTE_TITLE="Docker Note ${RAND_ID}"

echo "--- CONFIG ---"
echo "Email: $EMAIL"
echo "Title: $NOTE_TITLE"
echo "--------------"

echo -e "\n--- 1. REGISTER ---"
curl -s -X POST "$URL/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"username\": \"$USERNAME\", \"password\": \"$PASS\"}" | jq .

echo -e "\n\n--- 2. LOGIN ---"
LOGIN_RES=$(curl -s -X POST "$URL/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASS\"}")

ACCESS_TOKEN=$(echo $LOGIN_RES | jq -r '.access_token')
echo "Access Token acquired."

echo -e "\n--- 3. CREATE NOTE ---"

NOTE_RES=$(curl -s -X POST "$URL/notes/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"$NOTE_TITLE\", \"text\": \"Running inside a container with ID $RAND_ID!\", \"tags\": [\"devops\", \"test\"]}")
echo $NOTE_RES | jq .

NOTE_UUID=$(echo $NOTE_RES | jq -r '.uuid')

if [ "$NOTE_UUID" == "null" ]; then
  echo "CRITICAL ERROR: Note creation failed. Exiting."
  exit 1
fi

echo -e "\n--- 4. GET NOTE ---"
curl -s -X GET "$URL/notes/$NOTE_UUID" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .

echo -e "\n--- 5. UPDATE NOTE ---"
curl -s -X PATCH "$URL/notes/$NOTE_UUID" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Updated ${NOTE_TITLE}\", \"text\": \"Containers are awesome.\"}" | jq .

echo -e "\n--- 6. DELETE NOTE ---"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$URL/notes/$NOTE_UUID" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

if [ "$STATUS" -eq 204 ]; then
  echo "SUCCESS: Note deleted (204 No Content)."
  echo " MISSION ACCOMPLISHED"
else
  echo "FAIL: Failed to delete note. Status: $STATUS"
fi