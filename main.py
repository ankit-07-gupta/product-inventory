import uvicorn
import os
from fastapi import FastAPI,HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db
from .schema import Product as SchemaProduct
from .schema import ProductUpdate
from .models import Product as ModelProduct, Product
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.post('/product', response_model=SchemaProduct)
async def create_product(product_item: SchemaProduct):
    product_id = product_item.id
    if product_item.category or product_item.price or product_item.product or product_item.product_id:
        raise HTTPException(status_code=400, detail="Invalid Data")
    product = db.session.query(ModelProduct).filter(ModelProduct.id == product_id).first()
    if product is not None:
        raise HTTPException(status_code=500, detail="Product already exists!!!")
    db_product = ModelProduct(id=product_item.id, product=product_item.product, category=product_item.category, price=product_item.price)
    db.session.add(db_product)
    db.session.commit()
    raise HTTPException(status_code=200, detail="Product created")



@app.get('/all-products')
async def products():
    product = db.session.query(ModelProduct).all()
    if not product:
        raise HTTPException(status_code=404, detail="No products found")
    return product


@app.get('/products/{product_id}')
async def get_product(product_id: int):
    if product_id < 1:
        raise HTTPException(status_code=404, detail="Product ID is invalid!!!")

    product = db.session.query(ModelProduct).filter(ModelProduct.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.delete('/products/{product_id}')
async def delete_product(product_id: int):
    if product_id < 1:
        raise HTTPException(status_code=404, detail="Product ID is invalid!!!")

    product = db.session.query(ModelProduct).filter(ModelProduct.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.session.delete(product)
    db.session.commit()
    raise HTTPException(status_code=200, detail="Product deleted successfully")


@app.put("/products/{product_id}")
async def update_product(product_id: int, product_data: ProductUpdate):
    if product_id < 1:
        raise HTTPException(status_code=404, detail="Product ID is invalid!!!")

    product = db.session.query(ModelProduct).filter(ModelProduct.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    product.product = product_data.name
    product.category = product_data.category
    product.price = product_data.price
    db.session.add(product)
    db.session.commit()
    raise HTTPException(status_code=200, detail="Product updated successfully")


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
