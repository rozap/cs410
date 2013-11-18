import requests

__all__ = ['foo', 'bar' + 'baz', 'one', 'two']

def foo(x):
  r = requests.get('http://google.com')
  print r.content  
  return x



if __name__ == '__main__':
  foo(4)
