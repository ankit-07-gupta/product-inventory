# Install the required libraries for product-inventory app which is present in requirements.txt file . Command - pip install -r requirements.txt
# Main files to run the app is streamlit run productInventory.app and uvicorn main:app --reload
# Before running second step make sure database is connected with correct url and migration is done correctly 
DATABASE_URI = 'postgresql://postgres:<password>@localhost/<name_of_the_datbase>'
alembic init alembic
alembic revision --autogenerate -m "New Migration"
alembic upgrade head
# Backend and Frontend server is started succcessfully.
