#!/bin/bash
cd /c/Users/julie/gitRepos/trello_like

echo "=== TEST LOGIN ==="
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"user_name":"bob","user_password":"1234"}' \
  -c cookies.txt \
  -v

echo -e "\n\n=== TEST GET PROJECTS ==="
curl http://localhost:8000/api/projects/ \
  -b cookies.txt \
  -v
