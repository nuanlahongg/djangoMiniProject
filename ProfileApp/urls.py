from django.urls import path, include
from ProfileApp import view

urlpatterns = [
    path('home/', view.home, name='home'),

    path('index/', view.index, name='index'),
    path('userAuthen', view.userAuthen, name='userAuthen'),
    path('userLogout', view.userLogout, name='userLogout'),
    path('userChangePassword', view.userChangePassword, name='userChangePassword'),
    path('<userId>/userResetPassword', view.userResetPassword, name='userResetPassword'),

    path('spare_partList', view.spare_partList, name='spare_partList'),
    path('<pageNo>/spare_partListPage', view.spare_partListPage, name='spare_partListPage'),
    path('spare_partNew', view.spare_partNew, name='spare_partNew'),
    path('<spid>/spare_partUpdate', view.spare_partUpdate, name='spare_partUpdate'),
    path('<spid>/spare_partDelete', view.spare_partDelete, name='spare_partDelete'),

    path('adminList', view.adminList, name='adminList'),
    path('adminNew', view.adminNew, name='adminNew'),
    path('<aid>/adminUpdate', view.adminUpdate, name='adminUpdate'),
    path('<aid>/adminDelete', view.adminDelete, name='adminDelete'),

    path('memberList', view.memberList, name='memberList'),
    path('memberNew', view.memberNew, name='memberNew'),
    path('<mid>/memberOneshow', view.memberOneshow, name='memberOneshow'),
    path('<mid>/memberUpdate', view.memberUpdate, name='memberUpdate'),
    path('<mid>/memberDelete', view.memberDelete, name='memberDelete'),

    path('getjopList', view.getjopList, name='getjopList'),
    path('getjopNew', view.getjopNew, name='getjopNew'),
    path('<gid>/getjopUpdate', view.getjopUpdate, name='getjopUpdate'),
    path('<gid>/getjopDelete', view.getjopDelete, name='getjopDelete'),

    path('assignmentList', view.assignmentList, name='assignmentList'),
    path('assignmentMember', view.assignmentMember, name='assignmentMember'),
    path('assignmentNew', view.assignmentNew, name='assignmentNew'),
    path('<agid>/assignmentOneshow', view.assignmentOneshow, name='assignmentOneshow'),
    path('<agid>/assignmentUpdate', view.assignmentUpdate, name='assignmentUpdate'),
    path('<agid>/assignmentDelete', view.assignmentDelete, name='assignmentDelete'),

    path('savejobNew', view.savejobNew, name='savejobNew'),
    path('showAllsavejob', view.showAllsavejob, name='showAllsavejob'),
    path('<sid>/showsavejobDetail', view.showsavejobDetail, name='showOrderDetail'),

    path('pdfmemberReport', view.pdfmemberReport, name='pdfmemberReport'),
    path('pdfassignmentReport', view.pdfassignmentReport, name='pdfassignmentReport'),

    path('showSend', view.showSend, name='showSend'),
    path('<sid>/sandConfirm', view.sandConfirm, name='sandConfirm'),
]
