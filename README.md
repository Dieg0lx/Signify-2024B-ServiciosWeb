# Proyecto de Servicios Web
El proyecto consiste en una aplicación de autoaprendizaje enfocada en el lenguaje de señas.
La arquitectura de la aplicación está fragmentada en microservicios para optimizar el desarrollo y la escalabilidad.
A continuación se describen los microservicios que componen el sistema:

## Microservicios

### 1. Servicio de Gestión de Usuarios
- **Interfaz grafica:** [Flutter]
- **Servicio de nube:** [Amazon Web Service]
- **Lenguaje:** [Python]
- **Framework:** [Django]
- **Base de Datos:** [MySQL]
- **Descripción:**
 Este servicio se encarga de la administración de usuarios, incluyendo el registro, autenticación, y gestión de perfiles.
 Permite a los usuarios crear cuentas, iniciar sesión y actualizar su información personal.

*Tabla: usuarios*
| Columna         | Tipo de Dato    | Descripción                           |
|-----------------|-----------------|---------------------------------------|
| id            | INT (PK)      | Identificador único del usuario        |
| nombre        | VARCHAR(100)  | Nombre del usuario                     |
| correo        | VARCHAR(100)  | Correo electrónico del usuario         |
| contraseña    | VARCHAR(255)  | Contraseña del usuario (hashed)        |
| fecha_creacion| DATETIME      | Fecha y hora en que se creó la cuenta |
| activo        | BOOLEAN       | Estado de la cuenta (activo/inactivo) |

*Tabla: roles*
| Columna         | Tipo de Dato    | Descripción                           |
|-----------------|-----------------|---------------------------------------|
| id            | INT (PK)      | Identificador único del rol            |
| nombre        | VARCHAR(50)   | Nombre del rol                         |

*Tabla: usuario_roles*
| Columna         | Tipo de Dato    | Descripción                           |
|-----------------|-----------------|---------------------------------------|
| usuario_id    | INT (FK)      | Identificador del usuario              |
| rol_id        | INT (FK)      | Identificador del rol                  |

![Diagrama de servicio de gestion de usuarios](https://raw.githubusercontent.com/Dieg0lx/Proyecto-Servicios-Web/73697093b0311d188540745ed0c52e7e051a0b46/imgs_readme/tabla_1.png)

### 2. Servicio de Contenidos
- **Interfaz grafica:** [Flutter]
- **Servicio de nube:** [Amazon Web Service]
- **Lenguaje:** [Python]
- **Framework:** [Django]
- **Base de Datos:** [MySQL]
- **Descripción:**
 Este servicio maneja todo el contenido educativo relacionado con el lenguaje de señas. Administra recursos como videos, imágenes y textos educativos, y proporciona acceso a los materiales de aprendizaje para los usuarios.

*Tabla: contenidos*
| Columna         | Tipo de Dato    | Descripción                           |
|-----------------|-----------------|---------------------------------------|
| id            | INT (PK)      | Identificador único del contenido      |
| titulo        | VARCHAR(255)  | Título del contenido                   |
| descripcion   | TEXT          | Descripción del contenido              |
| tipo          | VARCHAR(50)   | Tipo de contenido (video, imagen, etc.)|
| url           | VARCHAR(255)  | URL del recurso                        |
| fecha_publicacion | DATETIME  | Fecha de publicación del contenido     |

*Tabla: categorias*
| Columna         | Tipo de Dato    | Descripción                           |
|-----------------|-----------------|---------------------------------------|
| id            | INT (PK)      | Identificador único de la categoría    |
| nombre        | VARCHAR(100)  | Nombre de la categoría                 |

*Tabla: contenido_categoria*
| Columna         | Tipo de Dato    | Descripción                           |
|-----------------|-----------------|---------------------------------------|
| contenido_id  | INT (FK)      | Identificador del contenido            |
| categoria_id  | INT (FK)      | Identificador de la categoría          |

### 3. Servicio de Evaluación
- **Interfaz grafica:** [Flutter]
- **Servicio de nube:** [Amazon Web Service]
- **Lenguaje:** [Python]
- **Framework:** [Django]
- **Base de Datos:** [MySQL]
- **Descripción:**
 Este servicio gestiona las evaluaciones y pruebas del usuario. Permite la creación, administración y seguimiento de evaluaciones, así como la calificación y retroalimentación sobre el desempeño del usuario.

*Tabla: evaluaciones*
| Columna         | Tipo de Dato    | Descripción                           |
|-----------------|-----------------|---------------------------------------|
| id            | INT (PK)      | Identificador único de la evaluación   |
| titulo        | VARCHAR(255)  | Título de la evaluación                |
| descripcion   | TEXT          | Descripción de la evaluación           |
| fecha_creacion| DATETIME      | Fecha de creación de la evaluación     |
| usuario_id    | INT (FK)      | Identificador del usuario evaluado     |

*Tabla: preguntas*
| Columna         | Tipo de Dato    | Descripción                           |
|-----------------|-----------------|---------------------------------------|
| id            | INT (PK)      | Identificador único de la pregunta     |
| evaluacion_id | INT (FK)      | Identificador de la evaluación         |
| texto         | TEXT          | Texto de la pregunta                  |

*Tabla: respuestas*
| Columna         | Tipo de Dato    | Descripción                           |
|-----------------|-----------------|---------------------------------------|
| id            | INT (PK)      | Identificador único de la respuesta    |
| pregunta_id   | INT (FK)      | Identificador de la pregunta           |
| texto         | TEXT          | Texto de la respuesta                 |

*Tabla: resultados*
| Columna         | Tipo de Dato    | Descripción                           |
|-----------------|-----------------|---------------------------------------|
| id            | INT (PK)      | Identificador único del resultado      |
| evaluacion_id | INT (FK)      | Identificador de la evaluación         |
| usuario_id    | INT (FK)      | Identificador del usuario              |
| calificacion  | FLOAT         | Calificación obtenida                  |
| fecha         | DATETIME      | Fecha en la que se realizó la evaluación|

### 4. Servicio de Notificaciones
- **Interfaz grafica:** [Flutter]
- **Servicio de nube:** [Amazon Web Service]
- **Lenguaje:** [Python]
- **Framework:** [Django]
- **Base de Datos:** [MySQL]
- **Descripción:**
 Este servicio se encarga de enviar notificaciones a los usuarios sobre eventos importantes, como actualizaciones de contenido, recordatorios de evaluaciones, y mensajes de interés general. Asegura que los usuarios se mantengan informados y comprometidos con la aplicación.

| Columna         | Tipo de Dato    | Descripción                           |
|-----------------|-----------------|---------------------------------------|
| id            | INT (PK)      | Identificador único de la notificación |
| usuario_id    | INT (FK)      | Identificador del usuario              |
| mensaje       | TEXT          | Contenido del mensaje                 |
| fecha_envio   | DATETIME      | Fecha y hora del envío de la notificación |
| leido         | BOOLEAN       | Estado de la notificación (leído/no leído) |
