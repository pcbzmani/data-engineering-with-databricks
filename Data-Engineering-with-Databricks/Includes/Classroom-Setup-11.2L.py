# Databricks notebook source
# MAGIC %run ./_utility-methods

# COMMAND ----------

DA = DBAcademyHelper(lesson="acls_lab")
DA.cleanup()
DA.init(create_db=False)
DA.conclude_setup()

# COMMAND ----------

def print_sql(self, rows, sql):
    displayHTML(f"""<body><textarea style="width:100%" rows={rows}> \n{sql.strip()}</textarea></body>""")

DBAcademyHelper.monkey_patch(print_sql)    

# COMMAND ----------

def generate_query(self):
    import re
    import random

    self.print_sql(23, f"""
CREATE DATABASE IF NOT EXISTS {DA.db_name}
LOCATION '{DA.paths.user_db}';

USE {DA.db_name};
    
CREATE TABLE beans 
(name STRING, color STRING, grams FLOAT, delicious BOOLEAN); 

INSERT INTO beans
VALUES ('black', 'black', {random.uniform(0, 5000):.2f}, {random.choice(["true", "false"])}),
       ('lentils', 'brown', {random.uniform(0, 5000):.2f}, {random.choice(["true", "false"])}),
       ('jelly', 'rainbow', {random.uniform(0, 5000):.2f}, {random.choice(["true", "false"])}),
       ('pinto', 'brown', {random.uniform(0, 5000):.2f}, {random.choice(["true", "false"])}),
       ('green', 'green', {random.uniform(0, 5000):.2f}, {random.choice(["true", "false"])}),
       ('beanbag chair', 'white', {random.uniform(0, 5000):.2f}, {random.choice(["true", "false"])}),
       ('lentils', 'green', {random.uniform(0, 5000):.2f}, {random.choice(["true", "false"])}),
       ('kidney', 'red', {random.uniform(0, 5000):.2f}, {random.choice(["true", "false"])}),
       ('castor', 'brown', {random.uniform(0, 5000):.2f}, {random.choice(["true", "false"])});

CREATE VIEW tasty_beans
AS SELECT * FROM beans WHERE delicious = true;
    """)

DBAcademyHelper.monkey_patch(generate_query)    

# COMMAND ----------

def generate_confirmation_query(self, username):
    import re
    clean_username = re.sub("[^a-zA-Z0-9]", "_", username)
    database = DA.db_name.replace(DA.clean_username, clean_username)
    
    self.print_sql(11, f"""
USE {database};

SELECT * FROM beans;
SELECT * FROM tasty_beans;
SELECT * FROM beans MINUS SELECT * FROM tasty_beans;

UPDATE beans
SET color = 'pink'
WHERE name = 'black'
""")

DBAcademyHelper.monkey_patch(generate_confirmation_query)    

# COMMAND ----------

def generate_union_query(self):
    self.print_sql(6, f"""
USE {DA.db_name};

SELECT * FROM beans
UNION ALL TABLE beans;""")

DBAcademyHelper.monkey_patch(generate_union_query)    

# COMMAND ----------

def generate_derivative_view(self):
    self.print_sql(7, f"""
USE {DA.db_name};

CREATE VIEW our_beans 
AS SELECT * FROM beans
UNION ALL TABLE beans;
""")

DBAcademyHelper.monkey_patch(generate_derivative_view)    

# COMMAND ----------

def generate_partner_view(self, username):
    import re
    clean_username = re.sub("[^a-zA-Z0-9]", "_", username)
    database = DA.db_name.replace(DA.clean_username, clean_username)
    
    self.print_sql(7, f"""
USE {database};

SELECT name, color, delicious, sum(grams)
FROM our_beans
GROUP BY name, color, delicious;""")

DBAcademyHelper.monkey_patch(generate_partner_view)    

# COMMAND ----------

def generate_delete_query(self, username):
    import re
    clean_username = re.sub("[^a-zA-Z0-9]", "_", username)
    database = DA.db_name.replace(DA.clean_username, clean_username)
    
    self.print_sql(5, f"""
USE {database};

DELETE FROM beans
    """)

DBAcademyHelper.monkey_patch(generate_delete_query)    

