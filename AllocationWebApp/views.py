import django_filters, csv, codecs, subprocess

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.template import RequestContext

from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Project, UserProfile, Csv, User, Instance, Preference, Allocation
from .forms import CsvModelForm, UserForm, UserProfileForm, SupervisorProjectForm, SupervisorProjectUpdate
from .utils import get_project, get_student_info

from subprocess import Popen, PIPE, TimeoutExpired
from sys import stderr, stdout

# Create your views here.
class Login(LoginView):
    template_name = 'AllocationWebApp/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('AllocationWebApp:projects')

class ProjectList(LoginRequiredMixin, ListView):
    # Model with all projects of any instance
    model = Project
    context_object_name = 'all-projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Projects with users instance
        user_profile = UserProfile.objects.get(user=self.request.user)
        instance = user_profile.instance
        context['projects'] = Project.objects.filter(instance=instance)

        # Search input
        search_input = self.request.GET.get('search-box') or ''
        if search_input:
            context['projects'] = context['projects'].filter(title__startswith=search_input)

        context['search_input'] = search_input

        return context

class SupervisorProjectList(LoginRequiredMixin, ListView):
    # Model with all projects of any instance
    model = Project
    context_object_name = 'all-projects'
    template_name = 'AllocationWebApp/supervisor_project_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Projects with users instance
        user_profile = UserProfile.objects.get(user=self.request.user)
        context['projects'] = Project.objects.filter(supervisor=user_profile)

        # Search input
        search_input = self.request.GET.get('search-box') or ''
        if search_input:
            context['projects'] = context['projects'].filter(title__startswith=search_input)

        context['search_input'] = search_input

        return context

class StudentList(LoginRequiredMixin, ListView):
    # Modle with all students of any instance
    model = UserProfile
    context_object_name = 'students'
    template_name = 'AllocationWebApp/student_list.html'

    def get_context_data(self, **kwargs):
        context = super(StudentList, self).get_context_data(**kwargs)

        # View all students of the same instance
        user_profile = UserProfile.objects.get(user=self.request.user)
        admin_instance = user_profile.instance
        context['students'] = context['students'].filter(user_type = 'Student', instance = admin_instance)

        # Search input
        search_input = self.request.GET.get('search-box') or ''
        if search_input:
            context['students'] = context['students'].filter(user__startswith=search_input)

        context['search_input'] = search_input

        return context

class ProjectView(LoginRequiredMixin, DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'AllocationWebApp/project_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project = get_object_or_404(Project, id=self.kwargs['pk'])
        user_profile = UserProfile.objects.get(user=self.request.user)

        is_favourite = False
        is_preference = False

        if project.favourite.filter(id=self.request.user.id).exists():
            is_favourite = True

        if Preference.objects.filter(student=user_profile, project=project).exists():
            is_preference = True

        context['is_favourite'] = is_favourite
        context['is_preference'] = is_preference

        return context

class StudentView(LoginRequiredMixin, DetailView):
    model = UserProfile
    context_object_name = 'student'
    template_name = 'AllocationWebApp/student_view.html'

class SupervisorProjectView(LoginRequiredMixin, DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'AllocationWebApp/supervisor_project.html'       

class StudentAllocationProjectView(LoginRequiredMixin, DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'AllocationWebApp/student_allocation_project.html'     

class PreferenceProjectView(LoginRequiredMixin, DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'AllocationWebApp/preference_project_view.html' 

class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['instance',  'supervisor', 'title', 'description', 'tags', 'seSuitable']
    success_url = reverse_lazy('AllocationWebApp:projects')

    def get_form(self, *args, **kwargs):
        form = super(ProjectCreate, self).get_form(*args, **kwargs)
        form.fields['supervisor'].queryset = UserProfile.objects.filter(user_type='Supervisor').all()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['create_view'] = True

        return context

class SupervisorProjectCreate(LoginRequiredMixin, CreateView):
    form_class = SupervisorProjectForm
    template_name = 'AllocationWebApp/supervisor_project_form.html'
    success_url = reverse_lazy('AllocationWebApp:supervisor-projects')

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        supervisor = UserProfile.objects.get(user=self.request.user)
        initial['supervisor'] = supervisor
        initial['instance'] = supervisor.instance
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['create_view'] = True

        return context

class ProjectEdit(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['instance', 'supervisor', 'title', 'description', 'tags', 'seSuitable']
    success_url = reverse_lazy('AllocationWebApp:projects')

    def get_form(self, *args, **kwargs):
        form = super(ProjectEdit, self).get_form(*args, **kwargs)
        form.fields['supervisor'].queryset = UserProfile.objects.filter(user_type='Supervisor').all()
        form.fields['instance'].queryset = Instance.objects.filter(name=UserProfile.objects.get(user=self.request.user).instance).all()
        return form

class SupervisorProjectEdit(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = SupervisorProjectUpdate
    template_name = 'AllocationWebApp/supervisor_project_form.html'
    success_url = reverse_lazy('AllocationWebApp:supervisor-projects')

class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    context_object_name = 'project'
    template_name = 'AllocationWebApp/project_delete.html'
    success_url = reverse_lazy('AllocationWebApp:projects')

class SupervisorProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    context_object_name = 'project'
    template_name = 'AllocationWebApp/supervisor_project_delete.html'
    success_url = reverse_lazy('AllocationWebApp:supervisor-projects')

class UserDelete(LoginRequiredMixin, DeleteView):
    model = UserProfile
    context_object_name = 'user'
    template_name = 'AllocationWebApp/user_delete.html'
    success_url = reverse_lazy('AllocationWebApp:students')

def preferences_list(request):
    current_user = request.user
    user_profile = UserProfile.objects.get(user=current_user)
    
    favourite_posts = list(current_user.favourite.all())
    preferences = [None] * 4
    preference_objects = Preference.objects.filter(student=UserProfile.objects.get(user=current_user)).all()

    for i in range(len(preference_objects)):
        preferences[i] = get_project(user_profile.id, i+1) 
        
    for project in favourite_posts:
        if project in preferences:
            project.favourite.remove(request.user)

    if request.method == 'POST':
        new_preferences = request.POST.get('project_list').split('.')
        del new_preferences[-1]

        no_of_preferences = 4

        # Loop through every preference
        for i in range(len(new_preferences)):
            project = Project.objects.get(title=new_preferences[i])

            if Preference.objects.filter(project=project, student=user_profile, preferenceNo=i+1):
                # Preference already exists
                pass 
            else:
                # Preference does not exist
                if Preference.objects.filter(student=user_profile, preferenceNo=i+1):
                    # If the user has a preference in that preferenceNo, update existing
                    Preference.objects.filter(
                        student=user_profile, 
                        preferenceNo=i+1
                    ).update(
                        project=project
                    )
                else:
                    # If the user does not have a preference in that preferenceNo, create new
                    Preference.objects.get_or_create(
                        instance = Instance.objects.get(name='Year 4'),
                        project = project,
                        student = user_profile,
                        preferenceNo = i+1,
                    )
                    project.favourite.remove(request.user)
        
        # If preference list not full
        if no_of_preferences > len(new_preferences):
            missing_preferences = no_of_preferences - len(new_preferences)
            # loop for missing preferences
            for i in range(missing_preferences):
                # delete preferences with indexes greater than the length of the preference list
                Preference.objects.filter(
                    student=user_profile, 
                    preferenceNo=len(new_preferences)+1+i
                ).delete()

        # Handling if user moves project from preferences to favourites
        favourites = request.POST.get('favourite_list').split('.')
        del favourites[-1]

        for i in range(len(favourites)):
            project = Project.objects.get(title=favourites[i])
            if project.favourite.filter(id=request.user.id).exists():
                pass # If favourite project already exists pass
            else:
                project.favourite.add(request.user) # Add project to favourites

    context = {
        'favourite_posts': favourite_posts,
        'preferences' : preferences,
    }

    return render(request, 'AllocationWebApp/preferences.html', context)

def favourite_post(request, id):
    project = get_object_or_404(Project, id=id)

    current_user = request.user
    user_profile = UserProfile.objects.get(user=current_user)

    if Preference.objects.filter(student=user_profile, project=project).exists():
        project.favourite.remove(request.user)

        preference = Preference.objects.get(student=user_profile, project=project)
        position = preference.preferenceNo
        preference.delete()

        for i in range(1,5):
            if i <= position:
                pass
            else:
                Preference.objects.filter(
                    student=user_profile,
                    preferenceNo=i
                ).update(
                    preferenceNo=i-1
                )

        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    if project.favourite.filter(id=request.user.id).exists():
        project.favourite.remove(request.user)
    else:
        project.favourite.add(request.user)

    
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST)
        user_form = UserForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)

            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors) 
        
        return redirect('AllocationWebApp:admin-panel')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {
        'user_form':user_form,
        'profile_form':profile_form,
        'registered':registered
    }

    return render(request, 'AllocationWebApp/register.html', context)

def admin_panel(request):
    return render(request, 'AllocationWebapp/admin_panel.html')

def upload_csv(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        form = CsvModelForm()
        file = Csv.objects.get(activated=False)

        with open(file.file_name.path, 'r', encoding='utf-8') as f:

            reader = csv.reader(f)

            for i, row in enumerate(reader):
                if i == 0:
                    pass
                else:
                    user_name = row[0]
                    user_email = row[1]
                    user_password = row[2]

                    new_user = User.objects.create_user(
                        username = user_name,
                        email = user_email,
                        password = user_password
                    )

                    user_instance = row[3]
                    user_user_type = row[4]

                    UserProfile.objects.create(
                        user = new_user,
                        instance = Instance.objects.get(name = user_instance),
                        user_type = user_user_type
                    )

            file.activated = True
            file.save()

    return render(request, 'AllocationWebapp/upload_csv.html', {'form': form})

def algorithms(request):
    return render(request, 'AllocationWebapp/algorithms.html')

# def populate_test(request):

#     students = UserProfile.objects.filter(user_type = 'Student').all()

#     student_1 = [2,3,10,1]
#     student_2 = [3,10,2,1,]
#     student_3 = [1,2,3,10]
#     student_4 = [10,1,3,2]
#     student_5 = [10,1,2,3]

#     i = 0
#     j = 0
#     k = 0
#     l = 0
#     m = 0

#     for preference in student_1:
#         Preference.objects.get_or_create(
#             instance = Instance.objects.get(name='Year 4'),
#             project = Project.objects.get(id=student_1[i]),
#             student = students[0],
#             preferenceNo = i+1,
#         )
#         i += 1
#     for preference in student_2:
#         Preference.objects.get_or_create(
#             instance = Instance.objects.get(name='Year 4'),
#             project = Project.objects.get(id=student_2[j]),
#             student = students[1],
#             preferenceNo = j+1,
#         )
#         j += 1
#     for preference in student_3:
#         Preference.objects.get_or_create(
#             instance = Instance.objects.get(name='Year 4'),
#             project = Project.objects.get(id=student_3[k]),
#             student = students[2],
#             preferenceNo = k+1,
#         )
#         k += 1
#     for preference in student_4:
#         Preference.objects.get_or_create(
#             instance = Instance.objects.get(name='Year 4'),
#             project = Project.objects.get(id=student_4[l]),
#             student = students[3],
#             preferenceNo = l+1,
#         )
#         l += 1
#     for preference in student_5:
#         Preference.objects.get_or_create(
#             instance = Instance.objects.get(name='Year 4'),
#             project = Project.objects.get(id=student_5[m]),
#             student = students[4],
#             preferenceNo = m+1,
#         )
#         m += 1

#     return render(request, 'AllocationWebapp/algorithms.html')

def cmd_line(request):

    # Get User Instance

    user_profile = UserProfile.objects.get(user=request.user)
    instance = user_profile.instance

    # Input file creation

    # File variables
    totalStudents = UserProfile.objects.filter(user_type = 'Student', instance=instance).count()
    totalProjects = Project.objects.filter(instance=instance).count()
    totalLecturers = UserProfile.objects.filter(user_type = 'Supervisor', instance=instance).count()

    students = UserProfile.objects.filter(user_type = 'Student', instance=instance).all()
    supervisors = UserProfile.objects.filter(user_type = 'Supervisor', instance=instance).all()
    projects = Project.objects.filter(instance=instance).all()

    # Dictionary Mapping
    student_map = dict(list(enumerate(students)))
    supervisor_map = dict(list(enumerate(supervisors)))
    project_map = dict(list(enumerate(projects)))

    # File handling
    input_filename = 'static/files/alg-file.txt'
    f = open(input_filename, 'w')

    # Students, Projects, Lecturers
    f.write(str(totalStudents) + ' ' + str(totalProjects) + ' ' + str(totalLecturers) + '\n')
    # Student: preferences
    for student in students:
        f.write(get_student_info(student, student_map, project_map, len(Preference.objects.filter(student=student))))
    # Projects: quota, quota, lecturer
    for project in projects:
        f.write(str(list(project_map.keys())[list(project_map.values()).index(project)]+1) + ': 0: 1: ' + str(list(supervisor_map.keys())[list(supervisor_map.values()).index(project.supervisor)]+1) + '\n')
    # Supervisors: quota, target, quota
    for supervisor in supervisors:
        f.write(str(list(supervisor_map.keys())[list(supervisor_map.values()).index(supervisor)]+1) + ': 0: 0: 5' + '\n')
    # Close file
    f.close()

    ################

    # Cmd Line Code

    TIMEOUT = 30*60 # in seconds (minutes * 60 seconds)

    args = ['python', 'AllocationWebApp/run_solver.py', '-f', 'static/files/alg-file.txt', '-na', '3', '-maxsize', '1', '-gen', '2'] # MAX 1 size, minimises 4th choice, minimises 3rd choice etc... Generous Alg
    cmdline = Popen(args, shell=True, stdout=subprocess.PIPE)

    try:
        out, err = cmdline.communicate(timeout=TIMEOUT)
    except:# TimeoutExpired:
        out = "tests timeout after " + str(TIMEOUT) + " seconds"
        err = "tests timeout after " + str(TIMEOUT) + " seconds"

    exitcode = cmdline.returncode

    ################

    # Output file to model

    output_filename = 'static/files/output.txt'
    with open(output_filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if ":" in line:
                line = line.strip()
                line = line.split(' ')

                line[0] = line[0].replace("s_","")
                line[0] = line[0].replace(":","")
                line[1] = line[0].replace("p_","")
                line[2] = line[0].replace("(l_","")
                line[2] = line[0].replace(")","")

                studentkey = line[0]
                projectkey = line[1]
                supervisorkey = line[2]

                Allocation.objects.get_or_create(
                    instance = Instance.objects.get(name='Year 4'),
                    student = student_map[int(studentkey)-1],
                    project = project_map[int(projectkey)-1],
                )

    info_filename = 'static/files/info.txt'
    with open(info_filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "cost:" in line:
                cost = line.replace("cost: ","")
            if "degree:" in line:
                degree = line.replace("degree: ","")
            if "profile:" in line:
                profile = line.replace("profile: < ","")
                profile = profile.replace(" >","")
        
        profile = profile.split(' ')

        output = []
        output.append("Algorithm cost: " + str(cost))
        output.append("Algorithm degree: " + str(degree))
        output.append(str(profile[0]) + " students got asigned their first choice")
        output.append(str(profile[1]) + " students got asigned their second choice")
        output.append(str(profile[2]) + " students got asigned their third choice")
        output.append(str(profile[3]) + " students got asigned their fourth choice")

        context={
            'output': output
        }

    return render(request, 'AllocationWebApp/algorithms.html', context)

def student_allocation(request):
    current_user = request.user
    user_profile = UserProfile.objects.get(user=current_user)

    if (Allocation.objects.filter(student = user_profile)):
        allocation_object = Allocation.objects.get(student = user_profile)

        context = {
            'project': allocation_object.project,
            'supervisor': allocation_object.project.supervisor
        }
    else:
        return render(request, 'AllocationWebApp/student_no_allocation.html')

    return render(request, 'AllocationWebApp/student_allocation.html', context)

def supervisor_allocations(request):
    supervisor = UserProfile.objects.get(user=request.user)
    supervisor_projects = Project.objects.filter(supervisor = supervisor).all()

    allocations = []

    for project in supervisor_projects:
        if Allocation.objects.filter(project=project).exists():
            allocations.append(Allocation.objects.get(project=project))

    print(supervisor_allocations)

    context = {
        'allocations' : allocations,
    }

    return render(request, 'AllocationWebApp/supervisor_allocations.html', context)

def stage_control(request):

    if request.method == 'POST':
        stage = request.POST.get('new_stage')

        user_profile = UserProfile.objects.get(user=request.user)
        instance = user_profile.instance

        Instance.objects.filter(
            name = instance
        ).update(
            stage = stage
        )


    return render(request, 'AllocationWebapp/stage_control.html')
