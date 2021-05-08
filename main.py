from fastapi import FastAPI, status
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
    ' ' || COALESCE(City, '') || ' ' || COALESCE(Country, '')) AS full_address FROM Customers ORDER BY CustomerID;
    ''').fetchall()
    return {
        "customers": [
            {
                "id": x['CustomerID'],
                "name": x['name'],
                "full_address": x['full_address']} for x in data]}

