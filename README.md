# Teleconsult DOST 2023

This is a Django-based teleconsultation system for DOST.

## Features
- Patient management
- Consultation scheduling  
- Mental health screening
- Appointment dashboard

## CI/CD Status
✅ Automated testing with GitHub Actions  
📊 Code coverage reporting  
🔄 Tests run on every push/PR  

## Getting Started

1. Clone the repository
2. Copy settings template: `copy Teleconsult\settings\local.py.example Teleconsult\settings\local.py` (Windows) or `cp Teleconsult/settings/local.py.example Teleconsult/settings/local.py` (Linux/Mac)
3. Edit `Teleconsult/settings/local.py` with your local database credentials
4. Set up virtual environment: `python -m venv venv`
5. Activate virtual environment: `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
6. Install dependencies: `pip install -r requirements.txt`
7. Run migrations: `python manage.py migrate`
8. Run tests: `python manage.py test`
9. Start server: `python manage.py runserver`

## Testing
- **186 tests** covering all major functionality
- Automatic testing on every push/PR
- Coverage reports generated automatically

## Development Workflow
1. Create feature branch from `develop`
2. Make changes and write tests
3. Push to GitHub (triggers CI)
4. Create Pull Request (CI must pass)
5. Merge after review

---
*Automated testing ensures code quality and prevents regressions.*