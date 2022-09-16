from util.db_conn import db_conn


@db_conn
def call_query(sql_query, cursor=None):
    """
    쿼리 실행 함수
    """
    cursor.execute(sql_query)
    data = cursor.fetchall()

    cursor.execute('SELECT @o')
    out_code = cursor.fetchone()
    out_code = out_code['@o']

    if out_code == 0:
        return data
    else:
        return []


@db_conn
def call_query_one(sql_query, cursor=None):
    """
    쿼리 실행 함수
    """
    cursor.execute(sql_query)
    data = cursor.fetchone()

    cursor.execute('SELECT @o')
    out_code = cursor.fetchone()
    out_code = out_code['@o']

    if out_code == 0:
        return data
    else:
        return []


@db_conn
def call_sp_drink_select(sp_args, cursor=None):
    """
    음료 선택
    """
    sp = 'CALL sp_drink_select(%(drink_id)s, %(customer_uuid)s, @o);'
    cursor.execute(sp, sp_args)
    data = cursor.fetchone()

    cursor.execute('SELECT @o')
    out_code = cursor.fetchone()
    out_code = out_code['@o']

    if out_code == 0:
        return data
    else:
        return []


@db_conn
def call_sp_drink_set(sp_args, cursor=None):
    """
    음료 인서트
    """
    sp = 'CALL sp_drink_set(%(drink_name)s,%(description)s,%(calorie)s,\
        %(manufacture)s,%(price)s,%(large_category)s,%(medium_category)s,\
        %(small_category)s,%(img)s,%(alcohol)s,%(measure)s,%(caffeine)s,\
        @drink_id, @o);'
    cursor.execute(sp, sp_args)

    cursor.execute('SELECT @o')
    out_code = cursor.fetchone()
    out_code = out_code['@o']

    cursor.execute('SELECT @drink_id')
    drink_id = cursor.fetchone()
    drink_id = drink_id['@drink_id']

    if out_code == 0:
        return drink_id
    else:
        return None


@db_conn
def call_sp_drink_comment_select(sp_args, cursor=None):
    """
    음료 리뷰 조회
    """
    sp = 'CALL sp_drink_comment_select(%(drink_id)s,\
        %(offset)s, %(limit)s, @o);'
    cursor.execute(sp, sp_args)
    data = cursor.fetchall()

    cursor.execute('SELECT @o')
    out_code = cursor.fetchone()
    out_code = out_code['@o']

    if out_code == 0:
        return data
    else:
        return []


@db_conn
def call_sp_drink_comment_set(sp_args, cursor=None):
    """
    음료 리뷰 등록
    """
    sp = 'CALL sp_drink_comment_select(%(drink_id)s,\
        %(customer_uuid)s, %(comment)s, %(score)s, @o);'
    cursor.execute(sp, sp_args)

    cursor.execute('SELECT @o')
    out_code = cursor.fetchone()
    out_code = out_code['@o']

    if out_code == 0:
        return True
    else:
        return False
