# Registration Management Odoo Module 📃🖋️

An Odoo module designed to simplify the management of registrations at a conference.
This Module offers the possibility to track registrations.

## Key Features 
- Manage registrations
- Email verification and SMS notification on user registration
- Assign reviewers to registrations

## Quick Start 

### Prerequisites 
- Docker and Docker Compose installed on your system 
- Odoo 15 Recommended (Works on version 16 and 17 too)
- Configure SMTP Server for email verifications (Optional )
- TWILIO API Key for SMS notifications (Optional )

### Steps to get Started 

#### 1. Clone the repository
```bash
git clone https://github.com/abdelkhalek-saadani/registration-manager-odoo.git
cd registration-manager
```

#### 2. Setup Environment Variables 
- Copy the example .env file: 

```bash
cp .env.example .env
```

#### 3. Start the Application 
- Run the following command to start Odoo and PostgreSQL:
```bash
docker compose up 
``` 
- Access Odoo in your browser at [http://localhost:8069](http://localhost:8069)

#### 4. Install the Module 
- Log in to Odoo with admin credentials (admin:admin by default) 
- Go to **Apps**, search for "registration_manager"
- Click **Install**


<!-- TODO: Add Module Overview Section in README, description for the models and views -->

<!-- Add screenshots to the module views-->
