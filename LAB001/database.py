import pymssql

from config import SQL_SERVER, SQL_DATABASE, SQL_USERNAME, SQL_PASSWORD


def conectar_sql():
    return pymssql.connect(
        server=SQL_SERVER,
        user=SQL_USERNAME,
        password=SQL_PASSWORD,
        database=SQL_DATABASE,
        port=1433,
        login_timeout=30,
        tds_version="7.4",
    )


def insert_photo_metadata(photo_data):
    conn = conectar_sql()
    cursor = conn.cursor()
    try:
        insert_query = """
            INSERT INTO dbo.Fotos (titulo, descricao, imagem_url)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (photo_data["titulo"], photo_data["descricao"], photo_data["imagem_url"]))
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()


def update_photo_metadata(photo_id, titulo, descricao):
    conn = conectar_sql()
    cursor = conn.cursor()
    try:
        update_query = """
            UPDATE dbo.Fotos
            SET titulo = %s, descricao = %s
            WHERE id = %s
        """
        cursor.execute(update_query, (titulo, descricao, photo_id))
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()


def delete_photo_metadata(photo_id):
    conn = conectar_sql()
    cursor = conn.cursor()
    try:
        delete_query = "DELETE FROM dbo.Fotos WHERE id = %s"
        cursor.execute(delete_query, (photo_id,))
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()


def list_photos_from_sql():
    conn = conectar_sql()
    cursor = conn.cursor()
    try:
        query = "SELECT id, titulo, descricao, data_upload, imagem_url FROM dbo.Fotos ORDER BY data_upload DESC"
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()
