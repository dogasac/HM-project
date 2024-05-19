from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",

    database="database"
)


cursor = mydb.cursor()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    sort_by = request.args.get('sort', 'price_asc')  # Fiyata göre varsayılan sıralama
    products = []
    categories = []

    cursor = mydb.cursor(dictionary=True)
 
    cursor.execute("SELECT c.name, COUNT(p.id) as count FROM categories c LEFT JOIN products p ON c.id = p.category_id GROUP BY c.id")
    categories = cursor.fetchall()

    order = 'ASC' if sort_by == 'price_asc' else 'DESC'
    if query:
        cursor.execute(f"SELECT * FROM products WHERE lower(name) LIKE %s ORDER BY price {order}", ('%' + query + '%',))
    else:
        cursor.execute(f"SELECT * FROM products ORDER BY price {order}")
    products = cursor.fetchall()

    cursor.close()

    return render_template('searches.html', products=products, query=query, categories=categories, sort_by=sort_by)

@app.route('/product/<int:product_id>', methods=['GET'])
def product(product_id):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()

    return render_template('product_detail.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)
