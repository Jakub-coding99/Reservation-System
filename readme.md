# Rezervační systém (ČEŠTINA)

Webová aplikace pro správu rezervací primárně po kadeřnické služby vytvořená ve Flasku.

---

## 📝 Popis projektu

Tato aplikace umožňuje uživateli vytvářet a spravovat rezervace přes webové rozhraní.  

- Frontend je napsaný v JavaScriptu, který zajišťuje dynamické ukládání a aktualizaci formulářů.
- Systém odesílá SMS připomínky klientům 24 hodin před plánovanou rezervací pomocí služby GoSMS API.

---

## 🖼️ Ukázky / Screenshots

**Přihlášení / Login**
![Image](https://github.com/user-attachments/assets/017e32bf-1bda-4dd3-bbac-7c13bef1cd3e)

**Hlavní stránka / Main page**

![Image](https://github.com/user-attachments/assets/429ed65f-584e-4e94-bba0-c7ffd74a8596)

**Úprava rezervace / Edit reservation**
![Image](https://github.com/user-attachments/assets/ed4faccb-207f-493f-ab8d-95e232b5a273)

**Responzivita / Responsive design**

![Image](https://github.com/user-attachments/assets/4375db10-b4c5-4952-aa75-711f915e4e7e)

![Image](https://github.com/user-attachments/assets/aa71981e-92a9-4d56-9098-d02a3feb022f)

---

## ⚙️ Použité technologie

- **Flask** – backend webového serveru
- **JavaScript** – dynamický frontend pro formuláře
- **GoSMS API** – odesílání SMS připomínek
- **SQLite** – databáze pro ukládání rezervací a uživatelů
- **HTML/CSS/Bootstrap5** 
---

## ✨ Funkce

- Uživatelský formulář pro vytváření a editaci rezervací
- Administrátorský login pro správu rezervací
- Automatické odesílání SMS připomínek 24 hodin před rezervací
- Dynamická aktualizace formulářů pomocí JavaScriptu bez nutnosti reloadu stránky
- Možnost vygenerování nového hesla přes email
- Připomenuté rezervace se automatický mažou 60minut po začátku rezervace.
- Responzivní pro mobilní zařízení
- SMS Log s informacemi o odeslání

---


## 🚀 Instalace

1. Klonuj repozitář
   ```bash
   git clone https://github.com/yourusername/your-flask-reservation-app.git
   ```

2. Nainstaluj
    ```bash
    pip install -r requirements.txt 
     ```
3. Zaregistruj se na GoSMS API a vytvoř ID a TOKEN 👉 [Klikni zde](https://www.gosms.eu/cs/api/?gad_source=1&gad_campaignid=22907436901&gbraid=0AAAAADlkV9Ol9BDYULsflk7r081PQlF-r&gclid=EAIaIQobChMI_bPApfGLkAMVF5qDBx3BCgwCEAAYASAAEgIa5_D_BwE)

4. Spusť 
     ```bash
    python main.py
     ```
---

# Reservation System (ENGLISH)

Web app for managing reservations, mainly designed for hair salon services, built with Flask.

---

## 📝 Project Description

This app allows users to create and manage reservations through a simple web interface.

- Frontend is written in JavaScript and handles dynamic saving and updating of forms.
- The system automatically sends SMS reminders to clients 24 hours before their reservation using the GoSMS API.

---


## ⚙️ Technologies Used

- **Flask** – backend web framework
- **JavaScript** – dynamic frontend handling
- **GoSMS API** – sending SMS reminders
- **SQLite** – database for storing users and reservations
- **HTML/CSS/Bootstrap 5** 

---

## ✨ Features

- User form to create and update reservations
- Admin login to manage all reservations
- Automatic SMS reminder 24 hours before the appointment
- JavaScript-powered form updates without page reload
- Password reset via email
- Automatically deletes past reservations 60 minutes after their start time
- Mobile-friendly design
- SMS log with delivery info

---

## 🚀 Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/your-flask-reservation-app.git
   ```

2. Install
    ```bash
    pip install -r requirements.txt 
     ```
3. Register to GoSMS API and create TOKEN and ID 👉 [Click here](https://www.gosms.eu/cs/api/?gad_source=1&gad_campaignid=22907436901&gbraid=0AAAAADlkV9Ol9BDYULsflk7r081PQlF-r&gclid=EAIaIQobChMI_bPApfGLkAMVF5qDBx3BCgwCEAAYASAAEgIa5_D_BwE)

4. Run
     ```bash
    python main.py
     ```
