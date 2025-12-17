import importlib
import seed_data

print("About to seed")
print("seed_data module file:", getattr(seed_data, '__file__', None))
print("seed_data contents:", dir(seed_data))
importlib.reload(seed_data)
print("After reload contents:", dir(seed_data))
if hasattr(seed_data, 'seed_database'):
	seed_data.seed_database()
	print("Done")
else:
	print("seed_database not found on seed_data module")
