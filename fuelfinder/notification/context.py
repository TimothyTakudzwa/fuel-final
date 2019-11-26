from .models import Notification


def notification_alert(request):
    notifications = False
    if request.user.is_authenticated:
        msgs = Notification.objects.filter(user=request.user, is_read=False)
        if msgs.exist():
            return {'notifications': notifications}
        else:
            return {
                'notifications': notifications,

            }
    else:
        return {}

