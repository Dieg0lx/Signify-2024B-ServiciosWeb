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

### 2. Servicio de Contenidos
- **Interfaz grafica:** [Flutter]
- **Servicio de nube:** [Amazon Web Service]
- **Lenguaje:** [Python]
- **Framework:** [Django]
- **Base de Datos:** [MySQL]
- **Descripción:**
 Este servicio maneja todo el contenido educativo relacionado con el lenguaje de señas. Administra recursos como videos, imágenes y textos educativos, y proporciona acceso a los materiales de aprendizaje para los usuarios.

### 3. Servicio de Evaluación
- **Interfaz grafica:** [Flutter]
- **Servicio de nube:** [Amazon Web Service]
- **Lenguaje:** [Python]
- **Framework:** [Django]
- **Base de Datos:** [MySQL]
- **Descripción:**
 Este servicio gestiona las evaluaciones y pruebas del usuario. Permite la creación, administración y seguimiento de evaluaciones, así como la calificación y retroalimentación sobre el desempeño del usuario.

### 4. Servicio de Notificaciones
- **Interfaz grafica:** [Flutter]
- **Servicio de nube:** [Amazon Web Service]
- **Lenguaje:** [Python]
- **Framework:** [Django]
- **Base de Datos:** [MySQL]
- **Descripción:**
 Este servicio se encarga de enviar notificaciones a los usuarios sobre eventos importantes, como actualizaciones de contenido, recordatorios de evaluaciones, y mensajes de interés general. Asegura que los usuarios se mantengan informados y comprometidos con la aplicación.
