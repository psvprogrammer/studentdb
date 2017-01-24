from django.db import connection
from django.shortcuts import render


class SqlDataMiddleware(object):
    def process_response(self, request, response):
        sqltime = 0
        for query in connection.queries:
            sqltime += float(query["time"])

        context = {
            'sql_time': sqltime,
            'sql_count': len(connection.queries),
        }
        sql_data = str(
            render(request, 'app/sql_data.html', context).content
        ).replace('\\n', '').replace('b\'', '')[:-1]
        response.content = str(
            response.content.decode()
        ).replace('</body>', sql_data + '</body>').encode()
        return response
