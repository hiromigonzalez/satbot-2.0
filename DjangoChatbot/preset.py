import docker

# Create a Docker client
client = docker.from_env()

# Define MySQL container configuration
container_config = {
    'image': 'mysql:latest',            # Use the latest MySQL image from Docker Hub
    'environment': {
        'MYSQL_ROOT_PASSWORD': 'preset2024',  # Set the root password for MySQL
        'MYSQL_DATABASE': 'mydatabase',     # Create a database named 'mydatabase'
    },
    'ports': {'3306/tcp': 3306},         # Map MySQL default port to host
    'detach': True,                      # Run container in detached mode
    'name': 'student_info_container'         # Name the container
}

# Create MySQL container
my_container = client.containers.run(**container_config)

create_db_commands = [
    "CREATE DATABASE mydatabase;"
    "USE mydatabase;",
    "CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255));",
    "INSERT INTO users (name, password, email) VALUES ('John Doe', 'pass5', 'john@example.com');",
    "INSERT INTO users (name, password, email) VALUES ('Jane Smith', 'pass5', 'jane@example.com');"
]

# Connect to MySQL and execute commands
db_commands = ";".join(create_db_commands)

exit_code, output = my_container.exec_run(f"mysql -uroot -ppreset2024 -e \"{db_commands}\"")
# if exit_code == 0:
#     print("Database created successfully.")
# else:
#     print("Failed to create database.")
#     print(output.decode())

# Print container ID
print("Container ID:", my_container.id)

