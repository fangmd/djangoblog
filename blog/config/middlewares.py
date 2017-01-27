from functools import reduce

import logging
from django.conf import settings
from django import http

from django.db import connection
from time import time
from operator import add
import re

# class AllowHostsMiddleware(object):
#     def process_request(self, request):
#         referer_url = request.META.get('HTTP_REFERER', '')
#         if referer_url.startswith(settings.ALLOWED_REFERER_URL):
#             return None
#         return http.HttpResponseForbidden('<h1>Forbidden</h1>')
from django.utils.deprecation import MiddlewareMixin
from django.utils.safestring import SafeText

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger("django")


class StatsMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        '''
        In your base template, put this:
        <div id="stats">
        <!-- STATS: Total: %(total_time).2fs Python: %(python_time).2fs DB: %(db_time).2fs Queries: %(db_queries)d ENDSTATS -->
        </div>
        '''

        # Uncomment the following if you want to get stats on DEBUG=True only
        # if not settings.DEBUG:
        #    return None

        # get number of db queries before we do anything
        n = len(connection.queries)

        # time the view
        start = time()
        response = view_func(request, *view_args, **view_kwargs)
        total_time = time() - start

        # compute the db time for the queries just run
        db_queries = len(connection.queries) - n
        if db_queries:
            db_time = reduce(add, [float(q['time'])
                                   for q in connection.queries[n:]])
        else:
            db_time = 0.0

        # and backout python time
        python_time = total_time - db_time

        stats = {
            'total_time': total_time,
            'python_time': python_time,
            'db_time': db_time,
            'db_queries': db_queries,
        }

        # replace the comment if found
        if response:
            try:
                # detects TemplateResponse which are not yet rendered
                if response.is_rendered:
                    rendered_content = response.content
                else:
                    rendered_content = response.rendered_content
            except AttributeError:  # django < 1.5
                rendered_content = response.content
            if rendered_content:

                if type(rendered_content) is not SafeText:
                    s = rendered_content.decode('utf-8')
                else:
                    s = rendered_content
                logger.debug('s ------------ type=' + str(type(s)))

                regexp = re.compile(
                    r'(?P<cmt><!--\s*STATS:(?P<fmt>.*?)ENDSTATS\s*-->)'
                )

                match = regexp.search(s)
                if match:
                    s = (s[:match.start('cmt')] +
                         match.group('fmt') % stats +
                         s[match.end('cmt'):])
                    response.content = s

        return response
