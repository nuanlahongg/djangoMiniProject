from django.forms import *
from .models import *
from django import forms


class Spare_partForm(forms.ModelForm):
    class Meta:
        model = Spare_part
        fields = ('spid', 'name', 'price', 'net', 'picture', )
        widgets = {
            'spid': forms.TextInput(attrs={'class': 'form-control',  'size':15, 'maxlength':13}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'size':55, 'maxlength':50}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'Min': 1}),
            'net': forms.NumberInput(attrs={'class': 'form-control', 'Min': 0}),
            'picture':forms.FileInput(attrs={'class': 'form-control', 'accept':'image/*'}),
        }
        labels = {
            'spid': 'รหัสอะไหล่',
            'name': 'ชื่ออะไหล่',
            'price': 'ราคา',
            'net': 'จำนวน',
            'picture': 'ภาพอะไหล่',
        }

    def updateForm(self):
        self.fields['spid'].widget.attrs['readonly'] = True
        self.fields['spid'].label = 'รหัสอะไหล่ [ไม่อนุญาตให้แก้ไขได้]'

    def deleteForm(self):
        self.fields['spid'].widget.attrs['readonly'] = True
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['price'].widget.attrs['readonly'] = True
        self.fields['net'].widget.attrs['readonly'] = True
        self.fields['picture'].widget.attrs['readonly'] = True


class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ('aid', 'name', 'birthdate', 'picture', 'password')
        widgets = {
            'aid': forms.TextInput(attrs={'class': 'form-control', 'size': 15, 'maxlength': 13}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'birthdate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date'}),
            'picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
        }

        labels = {
            'aid': 'รหัสเจ้าของร้าน',
            'name': 'ชื่อเจ้าของร้าน',
            'birthdate': 'วันเดือนปีเกิด',
            'picture': 'รูปเจ้าของร้าน',
            'password': 'รหัสผ่าน'
        }

    def updateForm(self):
        self.fields['aid'].widget.attrs['readonly'] = True
        self.fields['aid'].label = 'รหัสเจ้าของร้าน [ไม่อนุญาตให้แก้ไขได้]'
        self.fields['password'].widget = forms.HiddenInput()

    def deleteForm(self):
        self.fields['aid'].widget.attrs['readonly'] = True
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['birthdate'].widget.attrs['readonly'] = True
        self.fields['picture'].widget.attrs['readonly'] = True
        self.fields['password'].widget = forms.HiddenInput()

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('mid', 'name', 'birthdate', 'picture', 'password','address','tel')
        widgets = {
            'mid': forms.TextInput(attrs={'class': 'form-control', 'size': 15, 'maxlength': 13}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
            'birthdate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'tel': forms.TextInput(attrs={'class': 'form-control', 'size': 13, 'maxlength': 10}),
            'picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
        }

        labels = {
            'mid': 'รหัสช่าง',
            'name': 'ชื่อช่าง',
            'birthdate': 'วันเดือนปีเกิด',
            'picture': 'รูปเจ้าช่าง',
            'tel': 'เบอร์โทร',
            'address':'ที่อยู่',
            'password': 'รหัสผ่าน',
        }

    def updateForm(self):
        self.fields['mid'].widget.attrs['readonly'] = True
        self.fields['mid'].label = 'รหัสช่าง [ไม่อนุญาตให้แก้ไขได้]'
        self.fields['password'].widget = forms.HiddenInput()

    def deleteForm(self):
        self.fields['mid'].widget.attrs['readonly'] = True
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['birthdate'].widget.attrs['readonly'] = True
        self.fields['picture'].widget.attrs['readonly'] = True
        self.fields['address'].widget.attrs['readonly'] = True
        self.fields['tel'].widget.attrs['readonly'] = True
        self.fields['password'].widget = forms.HiddenInput()


class ChangePasswordForm(forms.Form):

    userId = forms.CharField(label='รหัสประจำตัวผู้ใช้', max_length=50,
                             widget=forms.TextInput(attrs={'class':'form-control', 'readonly':True}))
    oldPassword = forms.CharField(label='รหัสผ่านเดิม', max_length=100,
                                  widget=forms.PasswordInput(attrs={'class':'form-control'}))
    newPassword = forms.CharField(label='รหัสผ่านใหม่', max_length=100,
                                  widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirmPassword = forms.CharField(label='ยืนยันรหัสผ่านใหม่',  max_length=100,
                                      widget=forms.PasswordInput(attrs={'class':'form-control'}))

class ResetPasswordForm(forms.Form):
    userId = forms.CharField(label='รหัสประจำตัวผู้ใช้', max_length=50,
                             widget=forms.TextInput(attrs={'class':'form-control', 'readonly':True}))
    newPassword = forms.CharField(label='รหัสผ่านใหม่', max_length=100,
                                  widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirmPassword = forms.CharField(label='ยืนยันรหัสผ่านใหม่',  max_length=100,
                                      widget=forms.PasswordInput(attrs={'class':'form-control'}))

class GetjopForm(forms.ModelForm):
    class Meta:
        model = Getjop
        fields = ('gid', 'details', 'date', 'name_employer')
        widgets = {
            'gid': forms.TextInput(attrs={'class': 'form-control', 'size': 15, 'maxlength': 13}),
            'details': forms.TextInput(attrs={'class': 'form-control', 'size': 60, 'maxlength': 100}),
            'date': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date'}),
            'name_employer': forms.TextInput(attrs={'class': 'form-control', 'size': 55, 'maxlength': 50}),
        }
        labels = {
            'gid': 'รหัสการรับงาน',
            'details': 'รายละเอียด',
            'date': 'วันที่รับ',
            'name_employer': 'ชื่อผู้ว่าจ้าง',
        }
    def updateForm(self):
        self.fields['gid'].widget.attrs['readonly'] = True
        self.fields['gid'].label = 'รหัสการรับงาน [ไม่อนุญาตให้แก้ไขได้]'
    def deleteForm(self):
        self.fields['gid'].widget.attrs['readonly'] = True
        self.fields['details'].widget.attrs['readonly'] = True
        self.fields['date'].widget.attrs['readonly'] = True
        self.fields['name_employer'].widget.attrs['readonly'] = True

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('agid', 'member', 'getjop', 'date')
        widgets = {
            'agid': forms.TextInput(attrs={'class': 'form-control',  'size':15, 'maxlength':13}),
            'member': forms.Select(attrs={'class': 'form-control'}),
            'getjop': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date'}),

        }
        labels = {
            'agid': 'รหัสการหมอบหมายงาน',
            'member': 'รหัสช่าง',
            'getjop': 'รหัสงาน',
            'date': 'วันที่',
        }

    def updateForm(self):
        self.fields['agid'].widget.attrs['readonly'] = True
        self.fields['agid'].label = 'รหัสการหมอบหมายงาน [ไม่อนุญาตให้แก้ไขได้]'

    def deleteForm(self):
        self.fields['agid'].widget.attrs['readonly'] = True
        self.fields['member'].widget.attrs['readonly'] = True
        self.fields['getjop'].widget.attrs['readonly'] = True
        self.fields['date'].widget.attrs['readonly'] = True

class SavejobForm(forms.ModelForm):
    class Meta:
        model = Savejob
        fields = ('sid', 'spare_part', 'date', 'details')
        widgets = {
            'sid': forms.TextInput(attrs={'class': 'form-control',  'size':15, 'maxlength':13}),
            'spare_part': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date'}),
            'details': forms.TextInput(attrs={'class': 'form-control', 'size': 60, 'maxlength': 100}),


        }
        labels = {
            'sid': 'รหัสบันทึกงาน',
            'spare_part': 'รหัสอะไหล่',
            'date': 'วันที่',
            'details': 'รายละเอียดการซ่อม',
        }

    def deleteForm(self):
        self.fields['sid'].widget.attrs['readonly'] = True
        self.fields['spare_part'].widget.attrs['readonly'] = True
        self.fields['date'].widget.attrs['readonly'] = True
        self.fields['details'].widget.attrs['readonly'] = True