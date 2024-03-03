# class AuthRouter:
    
#     route_app_labels = {'auth', 'contenttypes', 'admin', 'sessions'}

#     def db_for_read(self, model, **hints):
        
#         if model._meta.app_label in self.route_app_labels:
#             return 'mysql'
#         return None

#     def db_for_write(self, model, **hints):
        
#         if model._meta.app_label in self.route_app_labels:
#             return 'mysql'
#         return None

#     def allow_relation(self, obj1, obj2, **hints):
        
#         if (
#             obj1._meta.app_label in self.route_app_labels or
#             obj2._meta.app_label in self.route_app_labels
#         ):
#             return True
#         return None

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
        
#         if app_label in self.route_app_labels:
#             return db == 'mysql'
#         return None


class CatalogRouter:
    route_app_labels = {'catalog'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'mongodb'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'mongodb'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'mongodb'
        return None


class CartRouter:
    route_app_labels = {'cart'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'mysql'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'mysql'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'mysql'
        return None