1. Start Docker Desktop
2. Run Docker Compose - docker-compose up --build
3. Run Database Migrations - docker-compose exec app alembic upgrade head
4. login into pgadmin
5. create a venv in python
6. pip install -r requirements.txt
7. alembic upgrade head
8. uvicorn app.main:app --fa
9. pytest to run tests
