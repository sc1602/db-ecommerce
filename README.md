# Flask Ecommerce

## Instalación

1. Clonar el repositorio
2. Instalar dependencias
    ```bash
    pip install -r requirements.txt
    ```
3. Crear un archivo `.env` con las variables de entorno
    ```bash
    DATABASE_URI='postgresql://user:password@localhost:5432/db_name'
    ```
4. Ejecutar migraciones
    ```bash
    flask db init # Inicializar la migración (Solo la primera vez)
    flask db migrate -m "Create tables" # Crear las migraciones
    flask db upgrade # Ejecutar las migraciones
    ```
5. Ejecutar el servidor
    ```bash
    python run.py
    ```