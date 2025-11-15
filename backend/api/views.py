from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Submission, Leaderboard
from .ml_scoring import evaluate_submission
from django.contrib.auth.models import User


@csrf_exempt
# @login_required
def submit(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method only"}, status=400)

    file = request.FILES["file"]
    score = evaluate_submission(file)
    # print(score)

    guest_user, _ = User.objects.get_or_create(username="guest", defaults={
        "email": "guest@example.com",
        "password": "test123",  
    })

    Submission.objects.create(user=guest_user, file=file, score=score)

    lb, _ = Leaderboard.objects.get_or_create(user=guest_user)
    if score > lb.best_score:
        lb.best_score = score
        lb.save()

    rank = list(Leaderboard.objects.order_by("-best_score")).index(lb) + 1

    return JsonResponse({"score": score, "rank": rank})


def leaderboard(request):
    data = [
        {
            "user": row.user.username,
            "score": row.best_score
        }
        for row in Leaderboard.objects.order_by("-best_score")
    ]
    return JsonResponse(data, safe=False)


def history(request):
    guest = User.objects.get(username="guest")  
    submissions = Submission.objects.filter(user=guest).order_by("-timestamp")

    data = [
        {
            "score": s.score,
            "file": s.file.name,
            "timestamp": s.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for s in submissions
    ]

    return JsonResponse(data, safe=False)
