from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()


class Customer(BaseModel):
    company_name: str


class Shipper(BaseModel):
    company_name: str


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


@app.get("/products")
async def products():
    cursor = app.db_connection.cursor()
    cursor.row_factory = lambda cursor, x: x[0]
    products = cursor.execute("SELECT ProductName FROM Products").fetchall()
    return {
        # "products": [x[0] for x in products],
        "products": products,
        "products_counter": len(products)
    }


@app.get("/suppliers/{supplier_id}")
async def single_supplier(supplier_id: int):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(
        "SELECT CompanyName, Address FROM Suppliers WHERE SupplierID = :supplier_id",
        {'supplier_id': supplier_id}).fetchone()

    return data


@app.get("/employee_with_region")
async def employee_with_region():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('''
        SELECT Employees.LastName, Employees.FirstName, Territories.TerritoryDescription 
        FROM Employees JOIN EmployeeTerritories ON Employees.EmployeeID = EmployeeTerritories.EmployeeID
        JOIN Territories ON EmployeeTerritories.TerritoryID = Territories.TerritoryID;
     ''').fetchall()
    return [{"employee": f"{x['FirstName']} {x['LastName']}", "region": x["TerritoryDescription"].strip()} for x in
            data]


@app.get("/employee_with_region_order")
async def employee_with_region():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('''
        SELECT Employees.LastName, Employees.FirstName, Territories.TerritoryDescription 
        FROM Employees JOIN EmployeeTerritories ON Employees.EmployeeID = EmployeeTerritories.EmployeeID
        JOIN Territories ON EmployeeTerritories.TerritoryID = Territories.TerritoryID
        ORDER BY Employees.LastName;
     ''').fetchall()
    return [{"employee": f"{x['FirstName']} {x['LastName']}", "region": x["TerritoryDescription"].strip()} for x in data]


@app.get("/customers")
async def customers():
    app.db_connection.row_factory = lambda cursor, x: x[0]
    customers = app.db_connection.execute("SELECT CompanyName FROM Customers").fetchall()
    return customers


# example of a wrong insert command, because of SQL Injection
@app.post("/customers/add_not_safe")
async def customers_add_not_safe(customer: Customer):
    cursor = app.db_connection.execute(
        f"INSERT INTO Customers (CompanyName) VALUES ('{customer.company_name}')"
    )
    # for 'insert' we have to commit!
    app.db_connection.commit()
    return {
        "CustomerID": cursor.lastrowid,
        "CompanyName": customer.company_name
    }


# example correct and safe insert command
@app.post("/customers/add")
async def customers_add(customer: Customer):
    cursor = app.db_connection.execute(
        "INSERT INTO Customers (CompanyName) VALUES {?}", (customer.company_name, )
    )
    app.db_connection.commit()
    new_customer_id = cursor.lastrowid
    app.db_connection.row_factory = sqlite3.Row
    customer = app.db_connection.execute(
        """SELECT CustomerID AS customer_id, CompanyName AS company_name
         FROM Customers WHERE CustomerID = ?""",
        (new_customer_id, )).fetchone()

    return customer


@app.patch("/shippers/edit/{shipper_id}")
async def shippers_add(shipper_id: int, shipper: Shipper):
    cursor = app.db_connection.execute(
        "UPDATE Shippers SET CompanyName = ? WHERE ShipperID = ?", (
            shipper.company_name, shipper_id)
    )
    app.db_connection.commit()
    shipper_id = cursor.lastrowid
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(
        """SELECT ShipperID AS shipper_id, CompanyName AS company_name
         FROM Shippers WHERE ShipperID = ?""",
        (shipper_id,)).fetchone()

    return data


@app.get("/orders")
async def orders():
    app.db_connection.row_factory = sqlite3.Row
    orders = app.db_connection.execute("SELECT * FROM Orders").fetchall()
    return {
        "orders_counter": len(orders),
        "orders": orders,
    }


@app.delete("/orders/delete/{order_id}")
async def order_delete(order_id: int):
    cursor = app.db_connection.execute(
        "DELETE FROM Orders WHERE OrderID = ?", (order_id,)
    )
    app.db_connection.commit()
    return {"deleted": cursor.rowcount}


@app.get("/region_count")
async def root():
    app.db_connection.row_factory = lambda cursor, x: x[0]
    regions = app.db_connection.execute(
        "SELECT RegionDescription FROM Regions ORDER BY RegionDescription DESC").fetchall()
    count = app.db_connection.execute('SELECT COUNT(*) FROM Regions').fetchone()

    return {
        "regions": regions,
        "regions_counter": count
    }


# task 4.1

@app.get("/categories", status_code=status.HTTP_200_OK)
async def categories():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('''
    SELECT CategoryID, CategoryName FROM Categories ORDER BY CategoryID;
    ''').fetchall()
    return {
        "categories": [
            {
                "id": x['CategoryID'], "name": x["CategoryName"]} for x in data]}


@app.get("/customers", status_code=status.HTTP_200_OK)
async def customers():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('''
    SELECT CustomerID, COALESCE(CompanyName, '') AS name, (COALESCE(Address, '') || ' ' || COALESCE(PostalCode, '') || 
    ' ' || COALESCE(City, '') || ' ' || COALESCE(Country, '')) AS full_address FROM Customers ORDER BY UPPER(CustomerID);
    ''').fetchall()
    return {
        "customers": [
            {
                "id": x['CustomerID'],
                "name": x['name'],
                "full_address": x['full_address']} for x in data]}


# task 4.2

@app.get("/products/{product_id}", status_code=status.HTTP_200_OK)
async def single_product(product_id: int):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(
        "SELECT ProductID, ProductName FROM Products WHERE ProductID = :product_id",
        {'product_id': product_id}).fetchone()

    if data:
        return {"id": data["ProductID"], "name": data["ProductName"]}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


# task 4.3

@app.get("/employees", status_code=status.HTTP_200_OK)
async def employees(limit: int = -1, offset: int = 0, order: str = 'EmployeeID'):

    dict_orders = {'EmployeeID': 'EmployeeID', 'first_name': 'FirstName', 'last_name': 'LastName', 'city': 'City'}
    if order not in dict_orders.keys():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    order = dict_orders[order]

    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(f'''
                        SELECT EmployeeID, LastName, FirstName, City
                        FROM Employees 
                        ORDER BY {order}
                        LIMIT ? 
                        OFFSET ?;''', (limit, offset)).fetchall()

    return {
        "employees": [
            {
                "id": x['EmployeeID'],
                "last_name": x['LastName'],
                "first_name": x['FirstName'],
                "city": x['City']} for x in data]}


# task 4.4

@app.get("/products_extended", status_code=status.HTTP_200_OK)
async def products_extended():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('''
    SELECT Products.ProductID, Products.ProductName, Categories.CategoryName, Suppliers.CompanyName 
    FROM Products
    JOIN Suppliers ON Products.SupplierID = Suppliers.SupplierID
    JOIN Categories ON Products.CategoryID = Categories.CategoryID;
    ''').fetchall()

    return {
        "products_extended":[
                {
                    "id": x['ProductID'],
                    "name": x['ProductName'],
                    "category": x['CategoryName'],
                    "supplier": x['CompanyName']} for x in data]}


# task 4.5

@app.get("/products/{product_id}/orders", status_code=status.HTTP_200_OK)
async def get_orders_by_id_product(product_id: int):
    app.db_connection.row_factory = sqlite3.Row
    product = app.db_connection.execute(
        "SELECT ProductID FROM Products WHERE ProductID = :product_id;", {'product_id': product_id}).fetchone()
    if not product:
        raise HTTPException(status_code=404, detail="Id not found")

    orders = app.db_connection.execute(f'''
        SELECT Orders.OrderID, Customers.CompanyName, od.Quantity, 
        ROUND((od.UnitPrice * od.Quantity) - (od.Discount * od.UnitPrice * od.Quantity), 2) AS total_price 
        FROM Orders JOIN 'Order Details' AS od on Orders.OrderID = od.OrderID 
        JOIN Products on od.ProductID = Products.ProductID
        LEFT JOIN Customers on Orders.CustomerID = Customers.CustomerID 
        WHERE Products.ProductID = {product_id} 
        ORDER BY Orders.OrderID;
        ''').fetchall()

    return {
        "orders": [
            {
                "id": x["OrderID"],
                "customer": x["CompanyName"],
                "quantity": x["Quantity"],
                "total_price": x["total_price"]} for x in orders]}


# task 4.6

class Category(BaseModel):
    name: str


@app.post("/categories", status_code=status.HTTP_201_CREATED)
async def categories_add(category: Category):
    cursor = app.db_connection.execute(
        "INSERT INTO Categories (CategoryName) VALUES (?)", (category.name, ))
    app.db_connection.commit()
    new_category_id = cursor.lastrowid
    app.db_connection.row_factory = sqlite3.Row
    category = app.db_connection.execute(
        """SELECT CategoryID AS id, CategoryName AS name
         FROM Categories WHERE CategoryID = ?""",
        (new_category_id, )).fetchone()

    return category


@app.put("/categories/{category_id}", status_code=status.HTTP_200_OK)
async def category_update(category: Category, category_id: int):
    cursor = app.db_connection.execute("""UPDATE Categories 
                                          SET CategoryName = ? 
                                          WHERE CategoryID = ?""", (category.name, category_id))
    app.db_connection.commit()
    cursor.row_factory = sqlite3.Row
    created_category = cursor.execute("""SELECT CategoryID AS id, CategoryName AS name 
                                         FROM Categories
                                         WHERE CategoryID = :id""", {"id": category_id}).fetchone()
    if created_category:
        return created_category
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.delete("/categories/{category_id}", status_code=status.HTTP_200_OK)
async def category_delete(category_id: int):
    cursor = app.db_connection.execute(
        "DELETE FROM Categories WHERE CategoryID = ?;", (category_id, )
    )
    app.db_connection.commit()

    if cursor.rowcount < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"deleted": cursor.rowcount}
