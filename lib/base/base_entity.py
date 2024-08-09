
class BaseEntity:

    def assign_values(self, details):
        """method to assign values using setters"""
        if not details:
            return
        for key, value in list(details.items()):
            setattr(self, key, value)