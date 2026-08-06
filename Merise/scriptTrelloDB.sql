CREATE DATABASE trellodb;

DROP TABLE IF EXISTS Tagged CASCADE;
DROP TABLE IF EXISTS Has_ CASCADE;
DROP TABLE IF EXISTS Task CASCADE;
DROP TABLE IF EXISTS Tag CASCADE;
DROP TABLE IF EXISTS Column_ CASCADE;
DROP TABLE IF EXISTS Project CASCADE;
DROP TABLE IF EXISTS User_ CASCADE;

CREATE TABLE User_(
   user_id SERIAL PRIMARY KEY,
   user_email VARCHAR(50) NOT NULL UNIQUE,
   user_password VARCHAR(255) NOT NULL
);

CREATE TABLE Project(
   project_id SERIAL PRIMARY KEY,
   project_name VARCHAR(50) NOT NULL,
   project_description VARCHAR(200),
   project_creation_date DATE NOT NULL,
   user_id INT NOT NULL,
   FOREIGN KEY(user_id) REFERENCES User_(user_id) ON DELETE CASCADE
);

CREATE TABLE Column_(
   column_id SERIAL PRIMARY KEY,
   column_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Task(
   task_id SERIAL PRIMARY KEY,
   task_name VARCHAR(50) NOT NULL,
   task_description VARCHAR(200) NOT NULL,
   task_dead_line DATE,
   task_order INT NOT NULL,
   column_id INT,
   project_id INT,
   FOREIGN KEY(column_id) REFERENCES Column_(column_id) ON DELETE SET NULL,
   FOREIGN KEY(project_id) REFERENCES Project(project_id) ON DELETE CASCADE
);

CREATE TABLE Tag(
   tag_id SERIAL PRIMARY KEY,
   tag_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Has_(
   project_id INT NOT NULL,
   column_id INT NOT NULL,
   has_order INT NOT NULL,
   PRIMARY KEY(project_id, column_id),
   FOREIGN KEY(project_id) REFERENCES Project(project_id) ON DELETE CASCADE,
   FOREIGN KEY(column_id) REFERENCES Column_(column_id) ON DELETE CASCADE
);

CREATE TABLE Tagged(
   task_id INT NOT NULL,
   tag_id INT NOT NULL,
   PRIMARY KEY(task_id, tag_id),
   FOREIGN KEY(task_id) REFERENCES Task(task_id) ON DELETE CASCADE,
   FOREIGN KEY(tag_id) REFERENCES Tag(tag_id) ON DELETE CASCADE
);

-- Test data
INSERT INTO User_ (user_email, user_password)
VALUES
('alice@example.com', 'alice_pwd'),
('bob@example.com', 'bob_pwd');

INSERT INTO Project (project_name, project_description, project_creation_date, user_id)
VALUES
('Roadmap Q3', 'Planification des fonctionnalites Q3', CURRENT_DATE, 1),
('Refonte UI', 'Refonte de l interface', CURRENT_DATE, 2);

INSERT INTO Column_ (column_name)
VALUES
('Backlog'),
('In Progress'),
('Done');

INSERT INTO Has_ (project_id, column_id, has_order)
VALUES
(1, 1, 1),
(1, 2, 2),
(1, 3, 3),
(2, 1, 1),
(2, 2, 2),
(2, 3, 3);

INSERT INTO Task (task_name, task_description, task_dead_line, task_order, column_id, project_id)
VALUES
('Creer API auth', 'Endpoints login et register', CURRENT_DATE + 7, 1, 1, 1),
('Configurer CI', 'Pipeline lint et tests', CURRENT_DATE + 5, 2, 2, 1),
('Polir page board', 'Ameliorer UX drag and drop', CURRENT_DATE + 10, 1, 2, 2),
('Deployer staging', 'Deploy auto sur branche develop', CURRENT_DATE + 14, 2, 3, 2);

INSERT INTO Tag (tag_name)
VALUES
('urgent'),
('frontend'),
('backend'),
('devops');

INSERT INTO Tagged (task_id, tag_id)
VALUES
(1, 3),
(1, 1),
(2, 4),
(3, 2),
(4, 4);

-- Validation queries
SELECT current_database();

SELECT task_id, task_name, project_id, column_id
FROM Task
ORDER BY task_id;

SELECT t.task_id, t.task_name, g.tag_name
FROM Tagged tg
JOIN Task t ON t.task_id = tg.task_id
JOIN Tag g ON g.tag_id = tg.tag_id
ORDER BY t.task_id, g.tag_name;
