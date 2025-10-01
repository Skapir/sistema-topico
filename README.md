# 📌 Sistema Tópico – CAP III EsSalud

**Sistema web para la gestión de pacientes y procedimientos en el área de Tópico.**  
Proyecto desarrollado como parte de la **Tesis de Suficiencia Profesional**.

---

## ✨ Características principales

- 📝 Registro digital de pacientes y procedimientos.
- 🔍 Búsqueda y actualización de datos desde **RENIEC / EsSalud**.
- 📊 Reportes de tiempos y estadísticas de atención.
- 👩‍⚕️ Optimización del flujo de trabajo de enfermería.
- 🌐 Desarrollado en **Django + TailwindCSS + MySQL**.

---

## 🛠️ Tecnologías usadas

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)  
![Django](https://img.shields.io/badge/Django-5.0-green?logo=django)  
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-38B2AC?logo=tailwindcss)  
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql)

---

## 🚀 Instalación y uso

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/Skapir/sistema-topico.git
   cd sistema-topico
   ```

2. Crear entorno virtual e instalar dependencias:

   ```bash
   python -m venv venv
   source venv/Scripts/activate   # en Windows
   pip install -r requirements.txt
   ```

3. Migrar base de datos:

   ```bash
   python manage.py migrate
   ```

4. Crear superusuario:

   ```bash
   python manage.py createsuperuser
   ```

5. Ejecutar el servidor:
   ```bash
   python manage.py runserver
   ```

---

## 📌 Estado del proyecto

Actualmente en desarrollo como parte de la **tesis profesional**.  
Se continuará optimizando con integración HL7 y automatización de flujos.

---

## 👨‍💻 Autor

**Sergio Pérez (Skapir)**  
📧 sperezdev@gmail.com
