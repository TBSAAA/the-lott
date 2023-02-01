import pymysql


def connect():
    # conect to mysql
    db = pymysql.connect(host='127.0.0.1',
                         port=13500,
                         user='jinri',
                         password='b590e929f506b99b82029b7d9148018b$HHR',
                         database='lott')
    # use cursor() create a cursor object
    cursor = db.cursor()
    return db, cursor


def get_data(query):
    db, cursor = connect()
    try:
        # execute SQL query
        cursor.execute(query)
        # close cursor
        db.close()
        return cursor.fetchall()
    except Exception as e:
        print("Error: unanle to get data: ", e)
        db.close()
        return None


def set_data(query):
    db, cursor = connect()
    db.begin()
    try:
        # execute SQL query
        cursor.execute(query)
        db.commit()

    except Exception as e:
        print("Error: unanle to set data: ", e)
        db.rollback()

    # close cursor
    db.close()


def update_data(query):
    db, cursor = connect()
    db.begin()
    try:
        # execute SQL query
        cursor.execute(query)
        db.commit()

    except Exception as e:
        print("Error: unanle to update data: ", e)
        db.rollback()

    # close cursor
    db.close()


def delete_data(query):
    db, cursor = connect()
    db.begin()
    try:
        # execute SQL query
        cursor.execute(query)
        db.commit()

    except Exception as e:
        print("Error: unanle to delete data: ", e)
        db.rollback()

    # close cursor
    db.close()


def set_many_data(query, data):
    db, cursor = connect()
    db.begin()
    try:
        # execute SQL query
        cursor.executemany(query, data)
        db.commit()

    except Exception as e:
        print("Error: unanle to set data: ", e)
        db.rollback()

    # close cursor
    db.close()


if __name__ == '__main__':
    # test
    query = "SELECT * from lott_draw ORDER BY Award_amount desc limit 100"
    # query = "select * from lott_draw"
    # print(get_data(query))
    data_list = get_data(query)
    for data in data_list:
        primary_number_list = data[2].split(',')
        # transform to int
        primary_number_list = [int(i) for i in primary_number_list]
        # list size
        primary_number_list_size = len(primary_number_list)
        print(primary_number_list_size)
