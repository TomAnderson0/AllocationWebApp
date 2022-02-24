from .models import Preference, UserProfile

def get_project(studentid, preferenceNo):
    
    try:
        student_projects = Preference.objects.filter(student = UserProfile.objects.get(id=studentid))
        preferenceno_project = student_projects.get(preferenceNo=preferenceNo)
        project = preferenceno_project.project
    except:
        return None

    return project

def get_student_info(student, student_map, project_map, preferences):

    student_id = str(list(student_map.keys())[list(student_map.values()).index(student)]+1)
    preference_list = []
    preference_str = ' '

    for i in range(preferences):
        preference_list.append(str(list(project_map.keys())[list(project_map.values()).index(get_project(student.id, i+1))]+1))

    print(preference_list)

    result = student_id + ': ' + preference_str.join(preference_list) + '\n'

    return result