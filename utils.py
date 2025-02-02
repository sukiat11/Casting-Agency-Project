import dateutil.parser
import babel
from flask import flash

#----------------------------------------------------------------------------#
# Utility Function
#----------------------------------------------------------------------------#
def flash_errors(form):
  errors = [f'{x}: {y}' for x,y in form.errors.items()]
  for error in errors:
    flash(f'Error:   {error}')

#----------------------------------------------------------------------------#
# Filters Utility Function
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')