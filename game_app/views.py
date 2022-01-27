from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Review, User, Game
from django.db.models import Q


def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
        return redirect ('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request,e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "You have successfully registered!")
        return redirect('/')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/games')

def show_all(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        logged_in_user = User.objects.get(id=request.session['user_id'])
        context = {
            'all_games': Game.objects.all(),
            'user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'show_all.html', context)

def show_page(request):
    return render(request,"add_game.html")

def show_reviewpg(request, game_id):
    context = {
        'game': Game.objects.get(id=game_id)
    }
    return render(request,"add_review.html", context)

def add_game(request):
    errors = Game.objects.game_validator(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request,e)
        return redirect('/games/page')
    else:
        print(request.POST)
        game = Game.objects.create(
            title = request.POST['title'],
            release = request.POST['release'],
            description = request.POST['description'],
            image = request.POST['image']
        )
    return redirect('/games')

def add_review(request, game_id):
    if request.method == "POST":
        review = Review.objects.create(
            creator = User.objects.get(id=request.session['user_id']),
            rating = request.POST.get('rating'),
            review = request.POST.get('review'),

            game_review = Game.objects.get(id=game_id)
        )
        return redirect(f"/games/{game_id}")

def show_one(request, game_id):
    print("GAME OBJECT", Game.objects.get(id=game_id).release)
    context = {
        'game': Game.objects.get(id=game_id),
        'all_reviews':Review.objects.filter(game_review=game_id)
        # 'review': Review.objects.get(id=review_id)
    }
    return render(request, "show_one.html", context)

def update(request, game_id):
    if request.method=="GET":
        context = {
            'game' : Game.objects.get(id=game_id),
        }
        return render(request,"show_one.html", context)
    errors = Game.objects.game_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/games/{game_id}")
    else:
        game = Game.objects.get(id=game_id)
        game.title = request.POST['title']
        game.release = request.POST['release']
        game.description = request.POST['description']
        game.image = request.POST['image']
        game.save()
        return redirect(f"/games")
    
def delete(request, game_id):
    game = Game.objects.get(id=game_id)
    game.delete()
    return redirect('/games')

def deletereview(request, review_id, game_id ):
    # game = Game.objects.get(id=game_id)
    review = Review.objects.get(id=review_id)
    review.delete()
    return redirect(f"/games/{game_id}")

def updatereview(request, review_id, game_id):
    if request.method=="GET":
        context = {
            'review' : Review.objects.get(id=review_id),
        }
        return render(request,"show_one.html", context)
    else:
        review = Review.objects.get(id=review_id)
        review.rating = request.POST['rating']
        review.review = request.POST['review']
        review.creator = User.objects.get(id=request.session['user_id'])
        review.game_review = Game.objects.get(id=game_id)
        review.save()
        return redirect(f"/games/{game_id}")

def showupdatereview(request, review_id, game_id):
    context = {
        'game': Game.objects.get(id=game_id),
        'review': Review.objects.get(id=review_id)
    }
    return render(request, "update_review.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    
    return render(request, 'success.html', context)


  
  



