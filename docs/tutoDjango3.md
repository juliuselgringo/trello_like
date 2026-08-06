# Dotenv

1. Installer dotenv dans venv
```
venv/Scripts/activate

python -m pip install python-dotenv
```

2. Dans backdjango/settings.py ajouter
```
import os
from dotenv import load_dotenv

load_dotenv()
```

