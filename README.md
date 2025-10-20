# 🏥 Patient Management System API (FastAPI)

## 📖 Introduction
This repository provides a **RESTful API** for managing patient records using **FastAPI**.  
It allows users to perform **CRUD operations** (Create, Read, Update, Delete) on patient data stored in a JSON file.  

This project is ideal for:
- Developers learning **FastAPI**  
- Building a **basic API** for patient management  
- Exploring **data validation** and **API design principles**

---

## 🚀 Overview
The API enables simple patient record management with FastAPI’s modern features, including:
- Input validation using **Pydantic**
- Auto-generated documentation via **Swagger UI**
- Persistent data storage in a **JSON file**

---

## ⚡ Quick Start

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Imsidd2002/Patient_Management_System_API-FastAPI.git
cd Patient_Management_System_API-FastAPI
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the API
```bash
uvicorn main:app --reload
```


## 📂 Repository Structure
```
Patient_Management_System_API-FastAPI/
├── main.py              # FastAPI application, API routes, data models, helper functions
├── patients.json        # Stores patient data in JSON format
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

---

## 🧰 Prerequisites

### Software
- Python **3.8+**
- **pip** (Python package installer)
- API testing tool — e.g. **curl**, **Postman**, or **web browser**

### Knowledge
- Basic understanding of **REST APIs**
- Familiarity with **Python**
- *(Optional)* Knowledge of **FastAPI** and **Pydantic**

---

## 🧑‍💻 Getting Started

1. **Clone the repository** (see Quick Start)  
2. **Install dependencies** using `pip`  
3. **Run the application** with `uvicorn`  
4. **Interact with Endpoints**  
   - Use tools like **Postman** or **curl** to perform CRUD operations on patient data.

---

## 🧾 Example Endpoints

| Method | Endpoint | Description |
|:------:|-----------|-------------|
| `GET` | `/patients` | Retrieve all patient records |
| `GET` | `/patients/{id}` | Retrieve a specific patient record |
| `POST` | `/patients` | Add a new patient record |
| `PUT` | `/patients/{id}` | Update an existing patient record |
| `DELETE` | `/patients/{id}` | Delete a patient record |

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).

---

## 💡 Author
**Siddharth Thakur**  
📧 [tsiddharth2002@gmail.com](mailto:tsiddharth2002@gmail.com)  
🔗 [GitHub: Imsidd2002](https://github.com/Imsidd2002)

---
