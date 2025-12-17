import importlib
import seed_data as sd

print('seed_data file:', getattr(sd, '__file__', None))
print('seed_data attrs:', [x for x in dir(sd) if not x.startswith('__')])
print('has seed_database:', hasattr(sd, 'seed_database'))
