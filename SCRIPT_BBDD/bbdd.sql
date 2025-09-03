-- Tabla para almacenar la información de los hoteles
CREATE TABLE Hotel (
    hotel_id INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(255),
    categoria VARCHAR(100)
);

-- Tabla para las habitaciones, relacionada con un hotel
CREATE TABLE Habitacion (
    habitacion_id INT PRIMARY KEY,
    hotel_id INT NOT NULL,
    tipo VARCHAR(100) NOT NULL,
    capacidad INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (hotel_id) REFERENCES Hotel(hotel_id)
);

-- Tabla para la información de los clientes
CREATE TABLE Cliente (
    cliente_id INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo_electronico VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20)
);

-- Tabla para gestionar las reservas, relacionando un cliente y una habitación
CREATE TABLE Reserva (
    reserva_id INT PRIMARY KEY,
    cliente_id INT NOT NULL,
    habitacion_id INT NOT NULL,
    fecha_entrada TIMESTAMP NOT NULL,
    fecha_salida TIMESTAMP NOT NULL,
    cantidad_personas INT NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES Cliente(cliente_id),
    FOREIGN KEY (habitacion_id) REFERENCES Habitacion(habitacion_id)
);