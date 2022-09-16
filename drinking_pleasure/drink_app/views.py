import jwt
import base64
from multiprocessing import AuthenticationError
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
import drink_app.call_sp as call_sp
from util.db_conn import db_conn


@db_conn
def sql_cursor(sql, sql_args, cursor=None):
    cursor.execute(sql, sql_args)
    rows = cursor.fetchall()
    return rows


JWT_SECRET_KEY = getattr(settings, 'SIMPLE_JWT', None)['SIGNING_KEY']

@permission_classes([AllowAny])
class DrinkGetList(APIView):
    def get(self, request):
        # SQL문 사용
        sql_query = "SELECT * \
            , IFNULL\
            ((SELECT AVG(score) FROM drink_comment WHERE drink_id=D.drink_id GROUP BY drink_id),0) AS score\
            FROM drink D;"
        _, rows = call_sp.call_query(sql_query)

        data_list = []
        for row in rows:
            data = dict()
            data["drink_id"] = row['drink_id']
            data["drink_name"] = row['drink_name']
            data["description"] = row['description']
            data["calorie"] = row['calorie']
            data["manufacture"] = row['manufacture']
            data["price"] = row['price']
            data["large_category"] = row['large_category']
            data["medium_category"] = row['medium_category']
            data["small_category"] = row['small_category']
            data["img"] = base64.decodebytes(row['img']).decode('latin_1')
            data["alcohol"] = row['alcohol']
            data["measure"] = row['measure']
            data["caffeine"] = row['caffeine']
            data["score"] = row['score']
            data_list.append(data)
        return JsonResponse({'data': data_list})


@authentication_classes([])
@permission_classes([])
class DrinkDetail(APIView):
    def get(self, request, pk):
        try:
            token = request.headers.get('token')
            user = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')

            customer_uuid = user['id']
        except Exception:
            customer_uuid = None

        sp_args = {
            'drink_id': pk,
            'customer_uuid': customer_uuid,
        }
        is_suc, data = call_sp.call_sp_drink_select(sp_args)
        if is_suc:
            data['img'] = base64.decodebytes(data['img']).decode('latin_1')

            sql_query = f'''UPDATE mazle.drink
                            SET views=views+1
                            WHERE drink_id={pk};'''
            call_sp.call_query(sql_query)

            return Response(status=status.HTTP_200_OK, data=data)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            token = request.headers.get('token')
            user = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
            customer_uuid = user['id']
            if not customer_uuid:
                raise AuthenticationError
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            drink_name = request.POST.get['drink_name']
            description = request.POST.get['description']
            calorie = request.POST.get['calorie']
            manufacture = request.POST.get['manufacture']
            price = request.POST.get['price']
            large_category = request.POST.get['large_category']
            medium_category = request.POST.get['medium_category']
            small_category = request.POST.get['small_category']
            img = request.FILES['img']
            alcohol = request.POST.get['alcohol']
            measure = request.POST.get['measure']
            caffeine = request.POST.get['caffeine']
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        sp_args = {
            'drink_name': drink_name,
            'description': description,
            'calorie': calorie,
            'manufacture': manufacture,
            'price': price,
            'large_category': large_category,
            'medium_category': medium_category,
            'small_category': small_category,
            'img': img,
            'alcohol': alcohol,
            'measure': measure,
            'caffeine': caffeine,
        }
        is_suc, drink_id = call_sp.call_sp_drink_set(sp_args)
        if is_suc:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([])
@permission_classes([])
class DrinkReview(APIView):
    def get(self, request, pk):
        try:
            offset = request.GET.get('offset')
            limit = request.GET.get('limit')
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        sp_args = {
            'drink_id': pk,
            'offset': offset,
            'limit': limit,
        }
        is_suc, data = call_sp.call_sp_drink_comment_select(sp_args)
        if is_suc:
            return Response(status=status.HTTP_200_OK, data=data)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, pk):
        try:
            token = request.headers.get('token')
            user = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
            customer_uuid = user['id']
            if not customer_uuid:
                raise AuthenticationError
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            comment = request.POST.get('comment')
            score = request.POST.get('score')
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        sp_args = {
            'customer_uuid': customer_uuid,
            'drink_id': pk,
            'comment': comment,
            'score': score,
        }
        is_suc, _ = call_sp.call_sp_drink_comment_set(sp_args)

        if is_suc:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            token = request.headers.get('token')
            user = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
            customer_uuid = user['id']
            if not customer_uuid:
                raise AuthenticationError
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        sql_delete = f"delete from drink_comment where drink_id={pk}\
             and customer_uuid={customer_uuid}"
        _, is_suc = call_sp.call_query_one(sql_delete)

        if is_suc:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([])
@permission_classes([])
class DrinkLike(APIView):

    def get(self, request, drink_id):
        '''
        유저가 해당 recipe_id에 좋아요 했는지 여부
        '''
        try:
            token = request.headers.get('token')
            user = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')

            customer_uuid = user['id']
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        sql_exist = f'''SELECT *
                        FROM drink_like
                        WHERE drink_id={drink_id}
                          AND customer_uuid={customer_uuid}'''
        is_suc, data = call_sp.call_query_one(sql_exist)
        if is_suc:
            return Response(status=status.HTTP_200_OK, data=data)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, drink_id):
        try:
            token = request.headers.get('token')
            user = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')

            customer_uuid = user['id']
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        sql_insert = f'''INSERT INTO drink_like(
                            drink_id
                          , customer_uuid
                        ) VALUES(
                            {drink_id}
                          , {customer_uuid});'''
        is_suc, _ = call_sp.call_query_one(sql_insert)
        if is_suc:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, drink_id):
        try:
            token = request.headers.get('token')
            user = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')

            customer_uuid = user['id']
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        sql_delete = f'''DELETE FROM drink_like
                         WHERE drink_id={drink_id}
                           AND customer_uuid={customer_uuid});'''
        is_suc, _ = call_sp.call_query_one(sql_delete)
        if is_suc:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([])
@permission_classes([])
class DrinkCommentLike(APIView):
    def get(self, request, comment_id):
        '''
        유저가 해당 comment에 좋아요 했는지 여부
        '''
        try:
            token = request.headers.get('token')
            user = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')

            customer_uuid = user['id']
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        sql_exist = f'''SELECT *
                        FROM drink_comment_like
                        WHERE comment_id={comment_id}
                          AND customer_uuid={customer_uuid}'''
        is_suc, data = call_sp.call_query_one(sql_exist)
        if is_suc:
            return Response(status=status.HTTP_200_OK, data=data)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, comment_id):
        try:
            token = request.headers.get('token')
            user = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')

            customer_uuid = user['id']
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        sql_insert = f'''INSERT INTO drink_comment_like(
                            comment_id
                          , customer_uuid
                        ) VALUES(
                            {comment_id}
                          , {customer_uuid});'''
        is_suc, _ = call_sp.call_query_one(sql_insert)
        if is_suc:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, comment_id):
        try:
            token = request.headers.get('token')
            user = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')

            customer_uuid = user['id']
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        sql_delete = f'''DELETE FROM drink_comment_like
                         WHERE comment_id={comment_id}
                           AND customer_uuid={customer_uuid});'''
        is_suc, _ = call_sp.call_query_one(sql_delete)
        if is_suc:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
