from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

import datetime
import time
import random

### Index page
def index(request):
    print '*'*20+" index "+'*'*20
    ### Get User Types
    c01=userType.objects.all()
    ### Context Info
    context = {
        "allUserType" : c01,
    }
    return render(request, "subApp1/index.html",context)

### Registration logic
def regUser(request):
    print '*'*20+" regUser "+'*'*20
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.person_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            ### Check User Type
            # print request.POST.get('inputUserType')
            if request.POST.get('inputUserType') == '0':
                errors["9error010"] = "Unable to register where user type is empty. Try again!"
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect('/')
            ### Check Email Duplication
            c11=Person.objects.filter(personEmail=request.POST.get('inputPersonEmail'))
            if len(c11) > 0:
                errors["9error011"] = "Unable to register with this person email address. Try again!"
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect('/')
            ### Generate College Email 
            temp_l = request.POST.get('inputLastName')
            temp_f = request.POST.get('inputFirstName')
            temp_cnt = 0
            while True:
                temp_cnt+=1
                ### Campus ID
                temp_n = str(random.randint(10,100))
                temp_email = temp_f[0].lower() + temp_l.lower() + temp_n + "@college.edu"
                print temp_email
                ### Try To Generate Campus ID For X Times
                if temp_cnt > 10:
                    errors["9error012"] = "Unable to register with this person. ERROR 1."
                    for tag, error in errors.iteritems():
                        messages.error(request, error, extra_tags=tag)
                    return redirect('/')
                    break
                c12=Person.objects.filter(collegeEmail=temp_email)
                if len(c12) == 0:
                    break
            ### End While Loop
            ### Generate Campus ID
            temp_year = str(datetime.date.today().year)
            temp_cnt = 0
            while True:
                temp_cnt+=1
                ### College Email Address
                temp_n = str(random.randint(1000,9999))
                temp_id = "#" + temp_year + temp_n
                print temp_id
                ### Try To Generate College Email Address For X Times
                if temp_cnt > 10:
                    errors["9error013"] = "Unable to register with this person. ERROR 2"
                    for tag, error in errors.iteritems():
                        messages.error(request, error, extra_tags=tag)
                    return redirect('/')
                    break
                ### Check If The Random College Email Address Found In DB
                c13=Person.objects.filter(campusID=temp_email)
                if len(c13) == 0:
                    break
            ### End While Loop
            ### Insert Person Into DB
            Person.objects.create(
                campusID=temp_id, 
                lastName=request.POST.get('inputLastName'),
                firstName=request.POST.get('inputFirstName'),
                dateBirth=request.POST.get('inputDateBirth'),
                address=request.POST.get('inputAddress'),
                phone=request.POST.get('inputPhone'),
                extNum=request.POST.get('inputExtNum'),
                personEmail=request.POST.get('inputPersonEmail'), 
                collegeEmail=temp_email,
                password=request.POST.get('inputPassword1'),
            )
            ### Get the Record
            c14=Person.objects.get(collegeEmail=temp_email)
            c15=userType.objects.get(id=request.POST.get('inputUserType'))
            print request.POST.get('inputUserType')
            ### Insert UserGroup Into DB
            userGroup.objects.create(person_ID=c14,userType_ID=c15)
            ### Insert Building Into DB
            Building.objects.create(
                ID_building=c14,
                buildingName=request.POST.get('inputBuilding'), 
                officeRoom=request.POST.get('inputOffice'), 
            )
            ### Create a Session 
            request.session['key']  = str(time.time()) + "-" + str(random.randint(1,99999))
            request.session['id']  = c14.id
            ### Generate a New Message for New User
            errors["9error014"] = "Your new campus ID is "+temp_id+", and your college email address is "+temp_email+". Please use your college email address for sign in. Thank you"
            ### Prepare Message For New User
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/dashboard')
    return redirect('/')

### Login Logic
def login(request):
    print '*'*20+" login "+'*'*20
    ### Get Input 
    temp_e = request.POST.get('inputCollegeEmail')
    temp_p = request.POST.get('inputPassword')
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.login_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            ### Check If College Email Exist
            c21 = Person.objects.filter(collegeEmail=temp_e)
            if len(c21) > 0:
                ### Get Password From DB
                c22 = Person.objects.get(collegeEmail=temp_e)
                ### Password Not Match
                if c22.password != temp_p:
                    errors["9error020"] = "Signed Failed! Invalid credentials!"
            else:
                ### College Email Not Found
                errors["9error021"] = "Signed Failed! Invalid credentials!"
            ### Prepare Error Messages
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect('/')
            else:
                ### Create A Session 
                request.session['key']  = str(time.time()) + "-" + str(random.randint(1,99999))
                request.session['id']  = c22.id
                return redirect('/dashboard')
    return redirect('/')

### System Page
def system(request):
    print '*'*20+" system "+'*'*20
    ### Check Session 
    if 'key' not in request.session:
        return redirect('/')
    ### Get All User Info
    c31=userType.objects.all()
    c32=MealCardType.objects.all()
    ### Context Info
    context = {
        "allUserType" : c31,
        "allMealType" : c32,
    }
    return render(request, "subApp1/system.html", context)

### Dashboard Page
def dashboard(request):
    print '*'*20+" dashboard "+'*'*20
    ### Check Session 
    if 'key' not in request.session:
        return redirect('/')
    ### Get All User Info
    c31=Person.objects.all()
    ### Context Info
    context = {
        "allPersons" : c31,
        "id" : request.session['id'] 
    }
    return render(request, "subApp1/dashboard.html", context)

### User Page
def user(request,userID):
    print '*'*20+" user "+'*'*20
    ### Check Session 
    if 'key' not in request.session:
        return redirect('/')
    ### Get the User Info
    c41=Person.objects.filter(id=userID)
    ### Calculate Age
    c42=Person.objects.get(id=userID)
    temp_today = datetime.datetime.now().date()
    temp_born = c42.dateBirth
    age = temp_today.year - temp_born.year - ((temp_today.month, temp_today.day) < (temp_born.month, temp_born.day))
    ### Get User Types
    c43=userGroup.objects.filter(person_ID=userID)

    ## Get Building Info
    c44=Building.objects.filter(ID_building=userID)
    ## Get Parking Info
    c45=Parking.objects.filter(ID_parking=userID)
    ## Get Meal Cards
    c46=MealCardType.objects.all()
    ## Get Meal Plans
    c47=MealGroup.objects.filter(ID_meal=userID)

    ### Get Building Types
    # c44=Building.objects.filter(ID_building=userID)
    ### Get User Types
    # c45=Parking.objects.filter(ID_parking=userID)
    ### Get User Types
    # c46=MealGroup.objects.filter(ID_meal=userID)
    ### Context Info
    context = {
        "id" : userID,
        "currentID": request.session['id'],
        "allPersons" : c41,
        "allUserGroup": c43,
        "allBuilding": c44,
        "allParking": c45,
        "allMealCards": c46,
        "allMeanPlans": c47,
        # "allBuildingGroup": c44,
        # "allParkingGroup": c45,
        # "allMealGroup": c46,
        "age" : age
    }
    return render(request, "subApp1/user.html", context)

### Add User Type Logic
def addUserType(request):
    print '*'*20+" addUserType "+'*'*20
    if 'key' not in request.session:
        return redirect('/')
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.userType_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/system')
        else:
            ### Insert Into DB
            userType.objects.create(
                nameType=request.POST.get('inputUserType'), 
            )
    return redirect('/system')

### Add User Group Logic
def addUserGroup(request,userID):
    print '*'*20+" addUserGroup "+'*'*20
    if 'key' not in request.session:
        return redirect('/')
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.userGroup_validator(request.POST)
        temp_group = request.POST.get('inputUserType')
        if str(temp_group) == '0':
            errors["9error030"] = "You did not selected a new user group."
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/services/'+userID)
        else:
            ### Get the Record
            c51=Person.objects.get(id=userID)
            c52=userType.objects.get(id=request.POST.get('inputUserType'))
            ### Insert UserType Into DB
            userGroup.objects.create(person_ID=c51,userType_ID=c52)
    return redirect('/services/'+userID)

### Add Services Page
def services(request,userID):
    print '*'*20+" services "+'*'*20
    ### Check Session 
    if 'key' not in request.session:
        return redirect('/')
    ### Check If Current User
    if str(request.session['id']) != str(userID):
        return redirect('/dashboard')
    ### Get the User Info
    c61=Person.objects.filter(id=userID)
    ### Get User Types
    c62=userType.objects.all()
    ### Get Group Types
    c63=userGroup.objects.filter(person_ID=userID)
    ### Filter Out UserType From GroupType
    c62a=set(c62)
    c63a=set(c63)
    for xx in c63a:
        # print xx.userType_ID.id
        c64=userType.objects.filter(id=xx.userType_ID.id)
        c62a=c62a.difference(c64)
    ## Get Building Info
    c65=Building.objects.filter(ID_building=userID)
    ## Get Parking Info
    c66=Parking.objects.filter(ID_parking=userID)
    ## Get Meal Cards
    c67=MealCardType.objects.all()
    ## Get Meal Plans
    c68=MealGroup.objects.filter(ID_meal=userID)
    ### Context Info
    context = {
        "id" : userID,
        "currentID": request.session['id'],
        "allPersons" : c61,
        "allUserType": c62a,
        "allUserGroup": c63,
        "allBuilding": c65,
        "allParking": c66,
        "allMealCards": c67,
        "allMeanPlans": c68,
    }
    return render(request, "subApp1/services.html", context)

### Add Meal Type Logic
def addMealType(request):
    print '*'*20+" addMealType "+'*'*20
    if 'key' not in request.session:
        return redirect('/')
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.mealType_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/system')
        else:
            ### Insert Into DB
            MealCardType.objects.create(
                CardType=request.POST.get('inputMealType'), 
                CardAmt=request.POST.get('inputMealAmt'), 
            )
    return redirect('/system')

### Add Meal Logic
def addMeal(request,userID):
    print '*'*20+" addMeal "+'*'*20
    if 'key' not in request.session:
        return redirect('/')
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.mealGroup_validator(request.POST)
        temp_group = request.POST.get('inputMealCard')
        if str(temp_group) == '0':
            errors["9error040"] = "You did not selected a new meal plan."
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/services/'+userID)
        else:
            ### Get the Record
            c71=Person.objects.get(id=userID)
            c72=MealCardType.objects.get(id=request.POST.get('inputMealCard'))
            ### Insert MealGroup Into DB
            MealGroup.objects.create(ID_meal=c71,ID_mealType=c72)
    return redirect('/services/'+userID)

### Add Building Office Logic
def addBuilding(request,userID):
    print '*'*20+" addBuilding "+'*'*20
    if 'key' not in request.session:
        return redirect('/')
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.building_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/services/'+userID)
        else:
            ### Get userID
            c81=Person.objects.get(id=userID)
            ### Insert Into DB
            Building.objects.create(
                ID_building=c81,
                buildingName=request.POST.get('inputBuilding'), 
                officeRoom=request.POST.get('inputOffice'), 
            )
    return redirect('/services/'+userID)

### Add Parking Logic
def addParking(request,userID):
    print '*'*20+" addParking "+'*'*20
    if 'key' not in request.session:
        return redirect('/')
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.parking_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/services/'+userID)
        else:
            ### Get userID
            c81=Person.objects.get(id=userID)
            ### Generate Random Permit No
            c82=get_random_string(length=15).upper()
            ### Insert Into DB
            Parking.objects.create(
                ID_parking=c81,
                plateNo=request.POST.get('inputPlateNo').upper(), 
                permitNo=c82, 
            )
    return redirect('/services/'+userID)

### Delete Person Group Logic
def deleteGroup(request,userID,noID):
    print '*'*20+" deleteGroup "+'*'*20
    if 'key' not in request.session:
        return redirect('/')
    ### Get and Delete - Person Group 
    if str(request.session['id']) == str(userID):
        c101=userGroup.objects.get(id=noID)
        c101.delete()
    return redirect('/services/'+userID)

### Delete Meal Group Logic
def deleteMeal(request,userID,noID):
    print '*'*20+" deleteMeal "+'*'*20
    if 'key' not in request.session:
        return redirect('/')
    ### Get and Delete - Meal Group 
    if str(request.session['id']) == str(userID):
        c111=MealGroup.objects.get(id=noID)
        c111.delete()
    return redirect('/services/'+userID)

### Delete Building Logic
def deleteBuilding(request,userID,noID):
    print '*'*20+" deleteBuilding "+'*'*20
    if 'key' not in request.session:
        return redirect('/')
    ### Get and Delete - Building 
    if str(request.session['id']) == str(userID):
        c121=Building.objects.get(id=noID)
        c121.delete()
    return redirect('/services/'+userID)

### Delete Parking Logic
def deleteParking(request,userID,noID):
    print '*'*20+" deleteParking "+'*'*20
    if 'key' not in request.session:
        return redirect('/')
    ### Get Parking 
    if str(request.session['id']) == str(userID):
        c131=Parking.objects.get(id=noID)
        c131.delete()
    return redirect('/services/'+userID)

### Update Phone Info
def updatePhone(request,userID):
    print '*'*20+" updatePhone "+'*'*20
    if 'key' not in request.session:
        return redirect('/')
    print userID
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.updatePhone_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/services/'+userID)
        else:
            c141=Person.objects.get(id=userID)
            c141.phone = request.POST.get('inputUpdatePhone')
            c141.save()
    ### 
    return redirect('/services/'+userID)

### Update Ext No
def updateExtNum(request,userID):
    print '*'*20+" updateExtNum "+'*'*20
    if 'key' not in request.session:
        return redirect('/')
    print userID
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.updateExtNum_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/services/'+userID)
        else:
            c151=Person.objects.get(id=userID)
            c151.extNum = request.POST.get('inputUpdateExtNum')
            c151.save()
    ### 
    return redirect('/services/'+userID)

### Update Person Email
def updatePersonEmail(request,userID):
    print '*'*20+" updatePersonEmail "+'*'*20
    if 'key' not in request.session:
        return redirect('/')
    print userID
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.updatePersonEmail_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/services/'+userID)
        else:
            c161=Person.objects.get(id=userID)
            c161.personEmail = request.POST.get('inputUpdatePersonEmail')
            c161.save()
    ### 
    return redirect('/services/'+userID)

### Logout
def logout(request):
    print '*'*20+" logout "+'*'*20
    ### Check Session 
    if 'key' not in request.session:
        return redirect('/')
    ### Remove Session 
    request.session.flush()
    return redirect('/')
