import datetime
import pandas as pd
import plotly.express as px
import picture
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from django.contrib.auth import logout
from django.forms import modelformset_factory
from django.shortcuts import render,redirect,get_object_or_404, HttpResponse

from django.contrib import messages
import datetime, os
from django.db.models import Q
from django.core.paginator import (Paginator, EmptyPage,PageNotAnInteger,)

from ProfileApp.forms import *
from ProfileApp.models import Spare_part, Admin, Member


# Create your views here.
def test(request):
    PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
    dir = PROJECT_PATH.split('\\')
    dir = dir[len(dir)-1]
    print(settings.BASE_DIR, ": ",  dir)

    return HttpResponse("")


def home(request):
    getjopAll = Getjop.objects.all()
    memberAll = Member.objects.all()
    spare_partAll = Spare_part.objects.all()
    getjopCount = len(getjopAll)
    memberCount = len(memberAll)
    spare_parCount = len(spare_partAll)
    spare_part = []
    amounts = []
    for item in spare_partAll:
        spare_part.append(item.name)
    # กรณีอ่านค่าจากบางฟิลด์ใน model มาใช้งาน
    spare_part = Spare_part.objects.values_list('name', 'net')
    df = pd.DataFrame(spare_part,  columns=['Spare_part', 'net'])

    fig = px.bar(df, x='Spare_part', y='net', title="แผนภูมิแท่งแสดงยอดจำนวนอะไหล่ที่มีอยู่")
    fig.update_layout(autosize=False, width=600, height=400,
                      margin=dict(l=10, r=10, b=100, t=100, pad=5),
                      paper_bgcolor="aliceblue", )
    chart = fig.to_html()
    context ={"spare_parCount":spare_parCount,
              "memberCount": memberCount,
              "getjopCount": getjopCount,
              'chart': chart
              }
    return render(request, "home.html", context)


def index(request):
    return render(request, 'index.html')


def spare_partList(request):
    spare_part = Spare_part.objects.all().order_by('spid')
    context = {'spare_part':spare_part}
    return render(request, 'crud/spare_partList.html', context)

def spare_partListPage(request, pageNo):
    # page = request.GET.get('page', page)
    items_per_page = 5
    spare_part = Spare_part.objects.all().order_by('spid')
    items_page = Paginator(spare_part, items_per_page)
    context = {'spare_part': items_page.page(pageNo)}
    return render(request, 'crud/spare_partListPage.html', context)

def spare_partNew(request):
    if request.method == 'POST':
        form = Spare_partForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            newForm = form.save(commit=False)
            spid = newForm.spid
            # filename = newForm.picture.name
            filepath = newForm.picture.name
            # point = filename.rfind('.')
            # ext = filename[point:]
            point = filepath.rfind('.')
            ext = filepath[point:]
            filenames = filepath.split('/')
            filename = filenames[len(filenames)-1]
            # filename = filename
            newfilename = spid + ext
            newForm.save() # product_tmp/xxx.xxx
            spare_part = get_object_or_404(Spare_part, spid=spid)
            spare_part.picture.name = '/SparePart/'+newfilename # pxxx.xxx
            spare_part.save()

            # บนเซิร์ฟเวอร์ต้องเป็น djangShopping/static/products/'
            # if os.path.exists('static/products/' + newfilename):
            #     os.remove('static/products/' + newfilename)  # file exits, delete it
            # os.rename('products_tmp/'+filename, 'static/products/' + newfilename)
            if os.path.exists('static/SparePart/' + newfilename):
                os.remove('static/SparePart/' + newfilename)  # file exits, delete it
            os.rename('static/SparePart/'+filename, 'static/SparePart/' + newfilename)
        else:
            spare_part = get_object_or_404(Spare_part, spid=request.POST['spid'])
            if spare_part:
                messages.add_message(request, messages.WARNING, "รหัสสินค้าซ้ำกับที่มีอยู่แล้วในระบบ")
                context = {'form': form}
                return render(request, 'crud/spare_partNew.html', context)
        return redirect('spare_partList')
    else:
        form = Spare_partForm()
        context = {'form':form }
        return render(request, 'crud/spare_partNew.html', context)

def spare_partUpdate(request, spid):
    spare_part = get_object_or_404(Spare_part, spid=spid)
    picture = spare_part.picture.name  # รูปสินค้าเดิม
    # form = ProductsForm(request.POST or None, instance=product, files=request.FILES)
    if request.method == 'POST':
        form = Spare_partForm(request.POST or None, instance=spare_part, files=request.FILES)
        if form.is_valid():
            newForm = form.save(commit=False)
            spid = newForm.spid
            print(newForm.picture.name)
            if newForm.picture.name != picture: #  หากเลือกรูปสินค้าใหม่
                newForm.save()
                filepath = newForm.picture.name
                point = filepath.rfind('.')
                ext = filepath[point:]
                filenames = filepath.split('/')
                filename = filenames[len(filenames) - 1]
                newfilename = spid + ext
                # filename = newForm.picture.name
                # point = filename.rfind('.')
                # ext = filename[point:]
                # newfilename =  spid + ext
                spare_part = get_object_or_404(Spare_part, spid = spid)
                spare_part.picture.name = '/SparePart/' +newfilename
                spare_part.save()
                # บนเซิร์ฟเวอร์ต้องเป็น djangShopping/static/products/'
                if os.path.exists('static/SparePart/' + newfilename): # file exits, delete it
                    os.remove('static/SparePart/' +newfilename)
                os.rename('static/SparePart/'+ filename, 'static/SparePart/' +newfilename)
            else:
                newForm.save()
        return redirect('spare_partList')
    else:
        # form = Spare_partForm(request.POST or None, instance=spare_part, files=request.FILES)
        form = Spare_partForm(instance=spare_part)
        form.updateForm()
        context = {'form': form}
        return render(request, 'crud/spare_partUpdate.html', context)

def spare_partDelete(request, spid):
    spare_part = get_object_or_404(Spare_part, spid=spid)
    picture = spare_part.picture.name  # รูปสินค้าเดิม
    if request.method == 'POST':
        spare_part.delete()
        # บนเซิร์ฟเวอร์ต้องเป็น djangShopping/static/products/'
        # ใน table db เก็บ /products/xxx.xx
        if os.path.exists('static'+picture):  # file exits, delete it
            os.remove('static'+picture)
        return redirect('spare_partList')
    else:
        form = Spare_partForm(instance=spare_part)
        form.deleteForm()
        context = {'form': form, 'spare_part':spare_part}
        return render(request, 'crud/spare_partDelete.html', context)


def adminList(request):
    admin = Admin.objects.all().order_by('aid')
    context = {'admin': admin}
    return render(request, 'crud/adminList.html', context)

def adminNew(request):
    if request.method == 'POST':
        form = AdminForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            newForm = form.save(commit=False)
            aid = newForm.aid
            # filename = newForm.picture.name
            filepath = newForm.picture.name
            # point = filename.rfind('.')
            # ext = filename[point:]
            point = filepath.rfind('.')
            ext = filepath[point:]
            filenames = filepath.split('/')
            filename = filenames[len(filenames) - 1]
            # filename = filename
            newfilename = aid + ext
            newForm.save()  # product_tmp/xxx.xxx
            admin = get_object_or_404(Admin, aid=aid)
            admin.picture.name = '/admin/' + newfilename  # pxxx.xxx
            admin.save()

            # บนเซิร์ฟเวอร์ต้องเป็น djangShopping/static/products/'
            # if os.path.exists('static/products/' + newfilename):
            #     os.remove('static/products/' + newfilename)  # file exits, delete it
            # os.rename('products_tmp/'+filename, 'static/products/' + newfilename)
            if os.path.exists('static/admin/' + newfilename):
                os.remove('static/admin/' + newfilename)  # file exits, delete it
            os.rename('static/admin/' + filename, 'static/admin/' + newfilename)
        else:
            admin = get_object_or_404(Admin, aid=request.POST['aid'])
            if admin:
                messages.add_message(request, messages.WARNING, "รหัสแอดมินซ้ำกับที่มีอยู่แล้วในระบบ")
                context = {'form': form}
                return render(request, 'crud/adminNew.html', context)
        return redirect('adminList')
    else:
        form = AdminForm()
        context = {'form': form}
        return render(request, 'crud/adminNew.html', context)

def adminUpdate(request, aid):
    admin = get_object_or_404(Admin, aid=aid)
    picture = admin.picture.name  # รูปสินค้าเดิม
    # form = ProductsForm(request.POST or None, instance=product, files=request.FILES)
    if request.method == 'POST':
        form = AdminForm(request.POST or None, instance=admin, files=request.FILES)
        if form.is_valid():
            newForm = form.save(commit=False)
            aid = newForm.aid
            print(newForm.picture.name)
            if newForm.picture.name != picture:  # หากเลือกรูปสินค้าใหม่
                newForm.save()
                filepath = newForm.picture.name
                point = filepath.rfind('.')
                ext = filepath[point:]
                filenames = filepath.split('/')
                filename = filenames[len(filenames) - 1]
                newfilename = aid + ext
                # filename = newForm.picture.name
                # point = filename.rfind('.')
                # ext = filename[point:]
                # newfilename =  spid + ext
                admin = get_object_or_404(Spare_part, aid=aid)
                admin.picture.name = '/admin/' + newfilename
                admin.save()
                # บนเซิร์ฟเวอร์ต้องเป็น djangShopping/static/products/'
                if os.path.exists('static/admin/' + newfilename):  # file exits, delete it
                    os.remove('static/admin/' + newfilename)
                os.rename('static/admin/' + filename, 'static/admin/' + newfilename)
            else:
                newForm.save()
        return redirect('adminList')
    else:
        # form = Spare_partForm(request.POST or None, instance=spare_part, files=request.FILES)
        form = AdminForm(instance=admin)
        form.updateForm()
        context = {'form': form}
        return render(request, 'crud/adminUpdate.html', context)

def adminDelete(request, aid):
    admin = get_object_or_404(Admin, aid=aid)
    picture = admin.picture.name  # รูปสินค้าเดิม
    if request.method == 'POST':
        admin.delete()
        # บนเซิร์ฟเวอร์ต้องเป็น djangShopping/static/products/'
        # ใน table db เก็บ /products/xxx.xx
        if os.path.exists('static' + picture):  # file exits, delete it
            os.remove('static' + picture)
        return redirect('adminList')
    else:
        form = AdminForm(instance=admin)
        form.deleteForm()
        context = {'form': form, 'admin': admin}
        return render(request, 'crud/adminDelete.html', context)

def memberList(request):
    member = Member.objects.all().order_by('mid')
    context = {'member': member}
    return render(request, 'crud/memberList.html', context)

def memberOneshow(request, mid):
    member = Member.objects.get(mid=mid)  # เช็ค pk
    context = {'member': member}
    return render(request, 'crud/memberOneshow.html', context)

def memberNew(request):
    if request.method == 'POST':
        form = MemberForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            newForm = form.save(commit=False)
            mid = newForm.mid
            # filename = newForm.picture.name
            filepath = newForm.picture.name
            # point = filename.rfind('.')
            # ext = filename[point:]
            point = filepath.rfind('.')
            ext = filepath[point:]
            filenames = filepath.split('/')
            filename = filenames[len(filenames) - 1]
            # filename = filename
            newfilename = mid + ext
            newForm.save()  # product_tmp/xxx.xxx
            member = get_object_or_404(Member, mid=mid)
            member.picture.name = '/member/' + newfilename  # pxxx.xxx
            member.save()

            # บนเซิร์ฟเวอร์ต้องเป็น djangShopping/static/products/'
            # if os.path.exists('static/products/' + newfilename):
            #     os.remove('static/products/' + newfilename)  # file exits, delete it
            # os.rename('products_tmp/'+filename, 'static/products/' + newfilename)
            if os.path.exists('static/member/' + newfilename):
                os.remove('static/member/' + newfilename)  # file exits, delete it
            os.rename('static/member/' + filename, 'static/member/' + newfilename)
        else:
            member = get_object_or_404(Member, mid=request.POST['mid'])
            if member:
                messages.add_message(request, messages.WARNING, "รหัสช่างกับที่มีอยู่แล้วในระบบ")
                context = {'form': form}
                return render(request, 'crud/memberNew.html', context)
        return redirect('memberList')
    else:
        form = MemberForm()
        context = {'form': form}
        return render(request, 'crud/memberNew.html', context)

def memberUpdate(request, mid):
    member = get_object_or_404(Member, mid=mid)
    picture = member.picture.name  # รูปสินค้าเดิม
    # form = ProductsForm(request.POST or None, instance=product, files=request.FILES)
    if request.method == 'POST':
        form = MemberForm(request.POST or None, instance=member, files=request.FILES)
        if form.is_valid():
            newForm = form.save(commit=False)
            mid = newForm.mid
            print(newForm.picture.name)
            if newForm.picture.name != picture:  # หากเลือกรูปสินค้าใหม่
                newForm.save()
                filepath = newForm.picture.name
                point = filepath.rfind('.')
                ext = filepath[point:]
                filenames = filepath.split('/')
                filename = filenames[len(filenames) - 1]
                newfilename = mid + ext
                # filename = newForm.picture.name
                # point = filename.rfind('.')
                # ext = filename[point:]
                # newfilename =  spid + ext
                admin = get_object_or_404(Spare_part, mid=mid)
                admin.picture.name = '/member/' + newfilename
                admin.save()
                # บนเซิร์ฟเวอร์ต้องเป็น djangShopping/static/products/'
                if os.path.exists('static/member/' + newfilename):  # file exits, delete it
                    os.remove('static/member/' + newfilename)
                os.rename('static/member/' + filename, 'static/member/' + newfilename)
            else:
                newForm.save()
        return redirect('memberList')
    else:
        # form = Spare_partForm(request.POST or None, instance=spare_part, files=request.FILES)
        form = MemberForm(instance=member)
        form.updateForm()
        context = {'form': form}
        return render(request, 'crud/memberUpdate.html', context)

def memberDelete(request, mid):
    member = get_object_or_404(Member, mid=mid)
    picture = member.picture.name  # รูปสินค้าเดิม
    if request.method == 'POST':
        member.delete()
        # บนเซิร์ฟเวอร์ต้องเป็น djangShopping/static/products/'
        # ใน table db เก็บ /products/xxx.xx
        if os.path.exists('static' + picture):  # file exits, delete it
            os.remove('static' + picture)
        return redirect('memberList')
    else:
        form = MemberForm(instance=member)
        form.deleteForm()
        context = {'form': form, 'member': member}
        return render(request, 'crud/memberDelete.html', context)

def userChangePassword(request):
    userId = request.session.get('userId')
    user = None
    if request.method == 'POST':
        form=ChangePasswordForm(request.POST or None)
        if request.session.get('userStatus') == 'member':
            user = get_object_or_404(Member, mid=userId)
        else:
            user = get_object_or_404(Admin, aid=userId)
        context = {'form': form}
        if request.POST['oldPassword'] == user.password:
            if request.POST['newPassword'] == request.POST['confirmPassword']:
                user.password = request.POST['newPassword']
                user.save()
                messages.add_message(request, messages.INFO, "เปลี่ยนรหัสผ่านเสร็จเรียบร้อย...")
                return redirect('home')
            else:
                messages.add_message(request, messages.WARNING, "รหัสผ่านใหม่กับรหัสที่ยืนยันไม่ตรงกัน...")
                return render(request, 'userChangePassword.html', context)
        else:
            messages.add_message(request, messages.ERROR, "รหัสผ่านที่ระบุไม่ถูกต้อง...")
            return render(request, 'userChangePassword.html', context)
    else:
        form=ChangePasswordForm(initial={'userId':userId})
        context ={'form':form}
        return render(request, 'userChangePassword.html', context)

def userResetPassword(request, userId):
    user = None
    if request.method == 'POST':
        form=ResetPasswordForm(request.POST or None)
        if request.session.get('userStatus') == 'member':
            user = get_object_or_404(Member, mid=userId)
        else:
            user = get_object_or_404(Admin, aid=userId)
        context = {'form': form}
        if request.POST['newPassword'] == request.POST['confirmPassword']:
            user.password = request.POST['newPassword']
            user.save()
            messages.add_message(request, messages.INFO, "เปลี่ยนรหัสผ่านเสร็จเรียบร้อย...")
            return redirect('home')
        else:
            messages.add_message(request, messages.WARNING, "รหัสผ่านใหม่กับรหัสที่ยืนยันไม่ตรงกัน...")
            return render(request, 'userResetPassword.html', context)
    else:
        form=ResetPasswordForm(initial={'userId':userId})
        context ={'form':form}
        return render(request, 'userResetPassword.html', context)


def userAuthen(request):
    if request.method == 'POST':
        userName = request.POST.get("userName")
        userPass = request.POST.get("userPass")
        user = Member.objects.filter(mid=userName).filter(password=userPass).first()
        # user = get_object_or_404(Customers, cid=userName, password=userPass)
        if user:
            request.session['userId'] = user.mid
            request.session['userName'] = user.name
            request.session['userStatus'] = 'member'
            # messages.add_message(request, messages.INFO, "Login success..")
            if request.session.get('orderActive'):
                del request.session['orderActive']
                return redirect('checkout')
            else:
                return redirect('home')
        else:
            user = Admin.objects.filter(aid=userName).filter(password=userPass).first()
            if user:
                request.session['userId'] = user.aid
                request.session['userName'] = user.name
                request.session['userStatus'] = 'admin'
                # messages.add_message(request, messages.INFO, "Login success..")
                return redirect('home')
            else:
                messages.add_message(request, messages.ERROR, "User or Password not Correct!!!..")
                data={'userName':userName}
                return render(request, 'userAuthen.html', data)
    else:
        data = {'userName': ''}
        return render(request, 'userAuthen.html', data)


def userLogout(request):
    logout(request)
    return redirect('index')

def getjopList(request):
    getjop = Getjop.objects.all().order_by('gid')
    context = {'getjop': getjop}
    return render(request, 'crud/getjopList.html', context)

def getjopNew(request):
    if request.method == 'POST':
        form = GetjopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('getjopList')
        else:
            context = {'form': form}
            return render(request, 'crud/getjopNew.html', context)
    else:
        form = GetjopForm()
        context = {'form': form}
        return render(request, 'crud/getjopNew.html', context)

def getjopUpdate(request, gid):
    getjop = get_object_or_404(Getjop, gid=gid)
    if request.method == 'POST':
        form = GetjopForm(request.POST or None, instance=getjop)
        if form.is_valid():
            form.save()
            return redirect('getjopList')
        else:
            context = {'form': form}
            return render(request, 'crud/getjopUpdate.html', context)
    else:
        form = GetjopForm(instance=getjop)
        form.updateForm()
        context = {'form': form,}
        return render(request, 'crud/getjopUpdate.html', context)

def getjopDelete(request, gid):
    getjop = get_object_or_404(Getjop, gid=gid)
    if request.method == 'POST':
        getjop.delete()
        return redirect('getjopList')
    else:
        form = GetjopForm(instance=getjop)
        form.deleteForm()
        context = {'form': form, 'getjop': getjop}
        return render(request, 'crud/getjopDelete.html', context)

def assignmentMember(request):
    assignment = Assignment.objects.all().order_by('agid')
    context = {'assignment': assignment}
    return render(request, 'assignmentMember.html', context)

def assignmentOneshow(request, agid):
    assignment = Assignment.objects.get(agid=agid)
    assignment = get_object_or_404(Assignment, agid=agid)
    confirmsAssignment = ConfirmsAssignment()
    confirmsAssignment.assignment = assignment
    confirmsAssignment.save()
    assignment.status = '2'
    assignment.save()
    # เช็ค pk
    context = {'assignment': assignment}
    return render(request, 'crud/assignmentOneshow.html', context)

def assignmentList(request):
    assignment = Assignment.objects.all().order_by('agid')
    context = {'assignment': assignment}
    return render(request, 'crud/assignmentList.html', context)

def assignmentNew(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assignmentList')
        else:
            context = {'form': form}
            return render(request, 'crud/assignmentNew.html', context)
    else:
        form = AssignmentForm()
        context = {'form': form}
        return render(request, 'crud/assignmentNew.html', context)

def assignmentUpdate(request, agid):
    assignment = get_object_or_404(Assignment, agid=agid)
    if request.method == 'POST':
        form = AssignmentForm(request.POST or None, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignmentList')
        else:
            context = {'form': form}
            return render(request, 'crud/assignmentUpdate.html', context)
    else:
        form = AssignmentForm(instance=assignment)
        form.updateForm()
        context = {'form': form,}
        return render(request, 'crud/assignmentUpdate.html', context)

def assignmentDelete(request, agid):
    assignment = get_object_or_404(Assignment, agid=agid)
    if request.method == 'POST':
        assignment.delete()
        return redirect('assignmentList')
    else:
        form = AssignmentForm(instance=assignment)
        form.deleteForm()
        context = {'form': form, 'assignment': assignment}
        return render(request, 'crud/assignmentDelete.html', context)

def savejobNew(request):
    if request.method == 'POST':
        form = SavejobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assignmentMember')
        else:
            context = {'form': form}
            return render(request, 'savejobNew.html', context)
    else:
        form = SavejobForm()
        context = {'form': form}
        return render(request, 'savejobNew.html', context)

def showAllsavejob(request):
    savejob = Savejob.objects.all().order_by('sid')
    context = {'savejob': savejob}
    return render(request, 'showAllsavejob.html', context)

def showsavejobDetail(request, sid):
    savejob = get_object_or_404(Savejob, sid=sid)
    if request.method == 'POST':
        return redirect('home')
    else:
        context = {'savejob': savejob}
        return render(request, 'showsavejobDetail.html', context)

def pdfmemberReport(request):
    pdfmetrics.registerFont(TTFont('THSarabunNew', 'thsarabunnew-webfont.ttf'))
    # pdfmetrics.registerFont(TTFont('THSarabunNew-Bold', 'thsarabunnew_bold-webfont.ttf'))
    template = get_template('pdfmemberReport.html')
    member=Member.objects.all()
    context = {"member": member}
    html = template.render(context)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    if not pdf.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("<h1><b>เกิดข้อผิดพลาด!!!</b> ไม่สามารถสร้างเอกสาร PDF ได้...</h2>", status=400)

def pdfassignmentReport(request):
    pdfmetrics.registerFont(TTFont('THSarabunNew', 'thsarabunnew-webfont.ttf'))
    # pdfmetrics.registerFont(TTFont('THSarabunNew-Bold', 'thsarabunnew_bold-webfont.ttf'))
    template = get_template('pdfassignmentReport.html')
    assignment=Assignment.objects.all()
    context = {"assignment": assignment}
    html = template.render(context)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    if not pdf.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("<h1><b>เกิดข้อผิดพลาด!!!</b> ไม่สามารถสร้างเอกสาร PDF ได้...</h2>", status=400)

def showSend(request):
    savejob = Savejob.objects.all().order_by('sid')
    context = {'savejob': savejob}
    return render(request, 'showSend.html', context)

def sandConfirm(request, sid):
    savejob = get_object_or_404(Savejob, sid=sid)
    confirm = Confirms()
    confirm.savejob = savejob
    confirm.save()
    savejob.status = '2'
    savejob.save()
    return redirect('showSend')