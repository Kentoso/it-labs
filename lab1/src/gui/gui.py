from service.database_service import AbstractDatabaseService, DatabaseService
from gui.view import View

if __name__ == "__main__":
    service: AbstractDatabaseService = DatabaseService()
    View(service)
