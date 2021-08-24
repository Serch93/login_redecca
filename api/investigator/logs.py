from api.investigator.models import ConnectionsLogs, Investigator


class LogsConnection:

    @classmethod
    def create_log_of_connection(cls, email, action):
        investigator, created = Investigator.objects.get_or_create(email=email)
        log = ConnectionsLogs(investigador=investigator, action=action)
        log.save()
        return log, created, investigator

    @classmethod
    def update_log_of_connection(cls, instance, status):
        instance.status_server = status
        instance.save()

    @classmethod
    def create_log_complete(cls, email, action, status):
        investigator, created = Investigator.objects.get_or_create(email=email)
        instance = ConnectionsLogs(
            investigador=investigator, action=action, status_server=status)
        instance.save()
