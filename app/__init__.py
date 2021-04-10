def __read_version_txt():
  import pkgutil
  return pkgutil.get_data('app', 'VERSION.txt').decode('utf-8').strip()

__version__ = __read_version_txt()
