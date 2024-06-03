import streamlit as st
import json
import requests
from schema import Product
from schema import ProductUpdate

st.title(' Product Inventory')

product_id = st.number_input(label='Product ID', step=1,key=0)
product_name = st.text_input(label='Product Name',key=1)
product_category = st.text_input(label='Product Category',key=2)
product_price = st.number_input(label='Product Price',key=3)

product = Product(id=product_id, product=product_name, category=product_category, price=product_price)
product_update = ProductUpdate(name=product_name, category=product_category, price=product_price)
product_dict = product.dict()
product_update_dict = product_update.dict()
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button('Add Product'):
        if product_id:
            url = 'http://0.0.0.0:8000/product'
            response = requests.post(url, json=product_dict)
            if response.status_code == 200:
                st.write(response.json()['detail'])
            if response.status_code == 500:
                st.write(response.json()['detail'])
            if response.status_code == 400:
                st.write("Product Details are Invalid")
with col2:
    if st.button('UpdateProduct by Id'):
        if product_id:
            url = f'http://0.0.0.0:8000/products/{product_id}'
            response = requests.put(url, json=product_update_dict)
            if response.status_code == 200:
                st.write(response.json()['detail'])
            if response.status_code == 404:
                st.write(response.json()['detail'])

with col3:
    if st.button('GetAll Products'):
        url = 'http://0.0.0.0:8000/all-products'
        response = requests.get(url)
        if response.status_code == 404:
            st.write(response.json()['detail'])
        if response.status_code == 200:
            data = json.loads(response.text)
            html_code_final = ""
            for x in data:
                html_code = "<ol>"
                for key, value in x.items():
                    res = key[0].upper() + key[1:]
                    html_code += f"<li><b>{res}:</b> {value}</li>"
                html_code += "</ol>"
                html_code_final += f'{html_code} <br>'
            st.html(html_code_final)

st.markdown("""---""")
product_id = st.number_input(label="Product ID", step=1, key=4)
col4, col5 = st.columns([1, 1])

with col4:
    if st.button('GetProduct by Id'):
        if product_id:
            url = f'http://0.0.0.0:8000/products/{product_id}'
            response = requests.get(url)
            if response.status_code == 404:
                st.write(response.json()['detail'])
            else:
                data = json.loads(response.text)
                html_code = "<ol>"
                for key, value in data.items():
                    res = key[0].upper() + key[1:]
                    html_code += f"<li><b>{res}:</b> {value}</li>"
                html_code += "</ol>"
                st.html(html_code)
with col5:
    if st.button('DeleteProduct by Id'):
        if product_id:
            url = f'http://0.0.0.0:8000/products/{product_id}'
            response = requests.delete(url)
            if response.status_code == 200:
                st.write(response.json()['detail'])
            if response.status_code == 404:
                st.write(response.json()['detail'])
