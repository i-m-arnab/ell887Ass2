from flask import Flask, render_template, request, redirect, url_for
import pyodbc

# Initialize Flask app
app = Flask(__name__)

# Initialize Azure SQL Database connection
# Replace the connection string with your Azure SQL Database credentials
conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=iitdelhicloudcomputing.database.windows.net;DATABASE=eet232756;UID=useradmin;PWD=Admin@1234'
connection = pyodbc.connect(conn_str)
cursor = connection.cursor()

@app.route('/')
def index():
    # Fetch all products from the database
    cursor.execute("SELECT *, (t.quantity * t.cost) total_cost FROM Products t")
    products = cursor.fetchall()
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Process form data and add product to the database
        name = request.form['name']
        description = request.form['description']
        company_name = request.form['company_name']
        quantity = request.form['quantity']
        cost = request.form['cost']
        # Add new product to the database
        cursor.execute("INSERT INTO Products (Name, Description, CompanyName, quantity, cost) VALUES (?, ?, ?, ?, ?)", (name, description, company_name, quantity, cost))
        connection.commit()
        # Redirect to the 'index' page after adding the product
        return redirect(url_for('index'))
    else:
        # Render the 'add_product' template for GET requests
        return render_template('product.html')

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if request.method == 'POST':
        try:
            # Execute SQL query to delete the product from the database
            cursor.execute("DELETE FROM Products WHERE Id = ?", (product_id,))
            connection.commit()  # Commit the transaction
            
            # Redirect to the 'index' page after deleting the product
            return redirect(url_for('index'))
        except Exception as e:
            # Handle any exceptions that occur during the database operation
            # You can log the error or render an error page
            return render_template('error.html', message="An error occurred while deleting the product.")


if __name__ == '__main__':
    app.run(debug=True)

#