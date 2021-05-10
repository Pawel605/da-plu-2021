from fastapi import FastAPI, status, HTTPException
import sqlite3

app = FastAPI()


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


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
                        OFFSET ?''', (limit, offset)).fetchall()

    return {
        "employees": [
            {
                "id": x['EmployeeID'],
                "last_name": x['LastName'],
                "first_name": x['FirstName'],
                "city": x['City']} for x in data]}
