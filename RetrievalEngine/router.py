from RetrievalEngine.settings import MANAGER_DB, ENGINE_DB


class RetrievalEngineDatabaseRouter:
    def db_for_read(self, model, **hints):
        return MANAGER_DB if model._meta.app_label == 'Manager' else ENGINE_DB

    def db_for_write(self, model, **hints):
        return MANAGER_DB if model._meta.app_label == 'Manager' else ENGINE_DB

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == MANAGER_DB:
            return False
        else:
            return app_label != 'Manager'




