# Εγκατάσταση

1. Φτιάξε και ενεργοποίησε ένα **virtual environment** με `python3.6`. Για οδηγίες του πώς να το κάνεις αυτό, δες [εδώ](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv).
1. Τρέξε το `pip install .[dev]`.
1. Κάνε αντιγραφή το *env.sample* στο *.env* και επεξεργάσου το *.env* για να προσαρμόσεις τις ρυθμίσεις στο τοπικό σου περιβάλλον.
1. Φτιάξε μία βάση MySQL και έναν χρήστη με πρόσβαση σε αυτήν και πείραξε την παράμετρο `DATABASE_URL` στο *.env* κατάλληλα (παραδείγματα [εδώ](https://github.com/kennethreitz/dj-database-url#url-schema)). Ίσως χρειαστεί κάποια βιβλιοθήκη για την επικοινωνία Python-MySQL (π.χ. `default-libmysqlclient-dev` για Linux).
1. Τρέξε τα migrations με `manage.py migrate`.