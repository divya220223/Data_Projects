import pymysql.cursors
from contextlib import contextmanager
from logging_setup import setup_logger


logger = setup_logger('db_helper')



@contextmanager
def get_db_cursor(commit=False):
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager",
        cursorclass = pymysql.cursors.DictCursor
    )

    cursor = connection.cursor()
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expense = cursor.fetchall()
        return expense


def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )


def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
    with get_db_cursor(commit=False) as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total 
               FROM expenses WHERE expense_date
               BETWEEN %s and %s  
               GROUP BY category;''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data


def fetch_expenses_by_month():
    logger.info(f"fetch_expenses_by_month")
    with get_db_cursor(commit=False) as cursor:
        cursor.execute(
            '''SELECT MONTH(expense_date)as Month, 
            MONTHNAME(expense_date)as Month_name, 
            SUM(amount)as total 
            FROM expenses            
            GROUP BY Month, Month_name;'''
        )
        rows = cursor.fetchall()

        return rows



if __name__ == "__main__":
    #expenses = fetch_expenses_for_date("2024-09-30")
    #print(expenses)
    # delete_expenses_for_date("2024-08-25")
    summary = fetch_expense_summary("2024-08-01", "2024-08-05")
    for record in summary:
        print(record)

    mon_exp = fetch_expenses_by_month()
    print(mon_exp)

