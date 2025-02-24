from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Connection to MySQL server
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="Inventory"
    )

# Home route
@app.route("/")
def home():
    return render_template('index.html')

@app.route('/product', methods=['GET', 'POST'])
def products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get search filters from the request
    search_id = request.args.get('search_id', '').strip()
    search_name = request.args.get('search_name', '').strip()

    # Query to fetch products
    query = """
        SELECT Product_ID, Product_Name, Product_In, Product_Out, 
               (Product_In - Product_Out) AS Product_Qty 
        FROM Product 
        WHERE 1=1
    """
    params = []

    # Apply filters if provided
    if search_id:
        query += " AND Product_ID LIKE %s"
        params.append(f"%{search_id}%")
    if search_name:
        query += " AND Product_Name LIKE %s"
        params.append(f"%{search_name}%")

    cursor.execute(query, params)
    products = cursor.fetchall()

    # Handle form submissions
    if request.method == 'POST':
        # Adding a New Product
        if 'add_product' in request.form:
            new_product_id = request.form.get('new_product_id')
            new_product_name = request.form.get('new_product_name')
            if new_product_id and new_product_name:
                cursor.execute("INSERT INTO Product (Product_ID, Product_Name, Product_In, Product_Out) VALUES (%s, %s, 0, 0)",
                            (new_product_id, new_product_name))
                conn.commit()
                return redirect(url_for('products'))

        # Updating Product Stock
        if 'update_product' in request.form:
            update_product_id = request.form.get("Product_ID")
            add_to_in = request.form.get('Product_in', '0')
            add_to_out = request.form.get('Product_Out', '0')

            if update_product_id and add_to_in.isdigit() and add_to_out.isdigit():
                add_to_in = int(add_to_in)
                add_to_out = int(add_to_out)

                # Fetch current stock values
                cursor.execute("SELECT Product_In, Product_Out FROM Product WHERE Product_ID = %s", (update_product_id,))
                product = cursor.fetchone()

                if product:
                    current_in = product["Product_In"]
                    current_out = product["Product_Out"]

                    new_in = current_in + add_to_in
                    new_out = current_out + add_to_out

                    # Ensure stock does not go negative
                    if new_out > new_in:
                        new_out = new_in  # Prevent negative stock

                    cursor.execute("UPDATE Product SET Product_In = %s, Product_Out = %s WHERE Product_ID = %s",
                                    (new_in, new_out, update_product_id))
                    conn.commit()

                return redirect(url_for('products'))

        # Editing Product Name
        if 'edit_product' in request.form:
            edit_product_id = request.form.get('edit_product_id')
            edit_product_name = request.form.get('edit_product_name')
            if edit_product_id and edit_product_name:
                cursor.execute("UPDATE Product SET Product_Name = %s WHERE Product_ID = %s",
                                (edit_product_name, edit_product_id))
                conn.commit()
                return redirect(url_for('products'))

        # Deleting a Product
        if 'delete_product' in request.form:
            delete_product_id = request.form.get('delete_product_id')
            if delete_product_id:
                cursor.execute("DELETE FROM Product WHERE Product_ID = %s", (delete_product_id,))
                conn.commit()
                return redirect(url_for('products'))

    # Close database connection
    cursor.close()
    conn.close()
    return render_template('product.html', products=products, search_id=search_id, search_name=search_name)


@app.route('/locations', methods=['GET', 'POST'])
def locations():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    search_loc_id = request.args.get('search_loc_id', '').strip()
    search_loc_name = request.args.get('search_loc_name', '').strip()

    query = "SELECT * FROM Location WHERE 1=1"
    params = []

    if search_loc_id:
        query += " AND Location_ID LIKE %s"
        params.append(f"%{search_loc_id}%")
    if search_loc_name:
        query += " AND Location_Name LIKE %s"
        params.append(f"%{search_loc_name}%")

    cursor.execute(query, params)
    locations = cursor.fetchall()

    # Handle Add Location
    if request.method == 'POST':
        if 'add_location' in request.form:
            new_location_id = request.form.get('new_location_id')
            new_location_name = request.form.get('new_location_name')
            if new_location_id and new_location_name:
                cursor.execute("INSERT INTO Location(Location_ID, Location_Name) VALUES(%s, %s)", 
                                (new_location_id, new_location_name))
                conn.commit()
                return redirect(url_for('locations'))

        # Handle Delete Location
        if 'delete_location' in request.form:
            delete_location_id = request.form.get('delete_location_id')
            cursor.execute("DELETE FROM Location WHERE Location_ID = %s", (delete_location_id,))
            conn.commit()
            return redirect(url_for('locations'))

        # Handle Edit Location
        if 'edit_location' in request.form:
            edit_location_id = request.form.get('edit_location_id')
            edit_location_name = request.form.get('edit_location_name')
            cursor.execute("UPDATE Location SET Location_Name = %s WHERE Location_ID = %s", 
                            (edit_location_name, edit_location_id))
            conn.commit()
            return redirect(url_for('locations'))

    cursor.close()
    conn.close()
    return render_template('location.html', locations=locations, search_loc_id=search_loc_id, search_loc_name=search_loc_name)


@app.route('/movements', methods=['GET', 'POST'])
def movements():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch all product movements
    cursor.execute("SELECT * FROM Product_Movement")
    movements = cursor.fetchall()

    # Fetch available locations for dropdown (excluding Central Warehouse)
    cursor.execute("SELECT * FROM Location WHERE Location_Name != 'Central Warehouse'")
    locations = cursor.fetchall()

    # Fetch products for dropdown
    cursor.execute("SELECT Product_ID, Product_Name, Product_In, Product_Out FROM Product")
    products = cursor.fetchall()

    message = request.args.get("message", "")

    if request.method == 'POST':
        from_loc = "Central Warehouse"
        to_loc = request.form['to_location']
        product_id = request.form['product_id']
        qty = int(request.form['quantity'])

        # Check stock availability
        cursor.execute("SELECT Product_In, Product_Out FROM Product WHERE Product_ID = %s", (product_id,))
        product = cursor.fetchone()

        if not product:
            return redirect(url_for('movements', message="Invalid Product ID"))

        product_in = product["Product_In"]  # This remains unchanged
        product_out = product["Product_Out"]

        # Calculate available balance quantity
        balance_qty = product_in - product_out
        if qty > balance_qty:
            return redirect(url_for('movements', message="Not enough stock in warehouse!"))

        # ✅ Only increase Product_Out, do not change Product_In
        cursor.execute("""
            UPDATE Product 
            SET Product_Out = Product_Out + %s 
            WHERE Product_ID = %s
        """, (qty, product_id))

        # Insert into Product_Movement table
        cursor.execute("""
            INSERT INTO Product_Movement (From_Location, To_Location, Product_ID, Quantity) 
            VALUES (%s, %s, %s, %s)
        """, (from_loc, to_loc, product_id, qty))

        conn.commit()
        return redirect(url_for('movements', message="Product moved successfully!"))

    cursor.close()
    conn.close()
    return render_template("movements.html", movements=movements, locations=locations, products=products, message=message)



        
        


if __name__ == '__main__':
    app.run(debug=True)

