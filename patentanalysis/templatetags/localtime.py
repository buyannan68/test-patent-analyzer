from django import template
import time
import pytz

register = template.Library()

@register.filter
def localtime(t1):
	# x = time.localtime(t1)
	# t2 = time.strftime('%Y-%m-%d %H:%M:%S', x)
	# return t2
	# return t1.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai'))
	return str(t1)[:5]