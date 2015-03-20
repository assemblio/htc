from flask import Blueprint, render_template, request, url_for, redirect
from flask.ext.security import current_user
from app.modules.public.mod_authentication.user_registration.model\
    import User, Experience, Education
from app.modules.public.mod_apply_for_job.model import Job
from app.modules.public.mod_apply_for_training.model import Training
from app.modules.public.mod_authentication.user_registration.form import\
    RegisterForm
from flask.ext.security import login_required
from bson import ObjectId

# Define the blueprint:
mod_profile = Blueprint('mod_profile', __name__)


# Set the route and accepted methods
@mod_profile.route('/profile')
@login_required
def profile():
    jobs_applied = current_user['jobs_applied']
    show_jobs = []
    if jobs_applied:
        for job in jobs_applied:
            show_jobs.append(Job.objects.get(id=job))

    trainings = current_user['trainings']
    show_trainings = []
    if trainings:
        for training in trainings:
            show_trainings.append(Training.objects.get(id=training))
    return render_template(
        'profile/index.html',
        current_user=current_user,
        show_jobs=show_jobs,
        show_trainings=show_trainings
    )


@mod_profile.route('/profile/<string:request_user>')
def get_user(request_user):
    user = User.objects.get(id=ObjectId(request_user))
    return render_template('profile/profile.html', username=user)


@mod_profile.route('/personal-info', methods=['POST', 'GET'])
@login_required
def update_personal_info():
    user_doc = User.objects.get(email=current_user.email)
    user_form = RegisterForm()

    if request.method == "GET":
        if current_user.is_authenticated():
            user_form.first_name.data = user_doc['first_name']
            user_form.last_name.data = user_doc['last_name']
            user_form.dateOfBirth.data = user_doc['dateOfBirth']
            user_form.email.data = user_doc['email']
            user_form.phone_mobile.data = user_doc['phone_mobile']
            user_form.phone_work.data = user_doc['phone_work']
            user_form.fax.data = user_doc['fax']
            user_form.address1.data = user_doc['address1']
            user_form.address2.data = user_doc['address2']
            user_form.expected_salary.data = user_doc['expected_salary']
            user_form.country.data=user_doc['country']
            user_form.stateProvince.data = user_doc['stateProvince']
            user_form.city.data = user_doc['city']
            user_form.zipCode.data = user_doc['zipCode']
            return render_template(
                'home/personal_info.html',
                form=user_form,
                action=url_for('mod_profile.update_personal_info'),
                display_pass_field=True
            )
        else:
            return render_template('home/index.html')
    elif request.method == "POST":
        user_doc.update(
            set__email=user_form.email.data,
            set__first_name=user_form.first_name.data,
            set__last_name=user_form.last_name.data,
            set__dateOfBirth=user_form.dateOfBirth.data,
            set__phone_mobile=user_form.phone_mobile.data,
            set__phone_work=user_form.phone_work.data,
            set__fax=user_form.fax.data,
            set__address1=user_form.address1.data,
            set__address2=user_form.address2.data,
            set__expected_salary=user_form.expected_salary.data,
            set__country=user_form.country.data,
            set__stateProvince=user_form.stateProvince.data,
            set__city=user_form.city.data,
            set__zipCode=user_form.zipCode.data
        )
        return redirect(url_for('mod_profile.update_education'))


@mod_profile.route('/update-education', methods=['POST', 'GET'])
@login_required
def update_education():
    user_form = RegisterForm()
    if request.method == 'GET':
        if current_user.is_authenticated():
            if current_user.education:
                for education in current_user.education:
                    user_form.school.data = education['school'].index
                    user_form.fieldOfStudy.data = education['fieldOfStudy'].index
                    user_form.schoolDegree.data = education['schoolDegree'].index
                    user_form.startDateSchool.data = education['startDateSchool'].index
                    user_form.endDateSchool.data = education['endDateSchool'].index
                    user_form.schoolDescription.data = education['schoolDescription'].index
                return render_template(
                    'home/update_education.html',
                    form=user_form,
                    action=url_for('mod_profile.update_education'),
                    display_pass_field=True
                )
            else:
                return render_template(
                    'home/update_education.html',
                    form=user_form,
                    action=url_for('mod_profile.update_education'),
                    display_pass_field=True
                )

        else:
            return render_template('home/index.html')
    elif request.method == 'POST':
        user_form_values = RegisterForm(request.form)
        user_doc = User.objects.get(email=current_user.email)
        education = Education(
            school=user_form_values.school.data,
            fieldOfStudy=user_form_values.fieldOfStudy.data,
            schoolDegree=user_form_values.schoolDegree.data,
            startDateSchool=user_form_values.startDateSchool.data,
            endDateSchool=user_form_values.endDateSchool.data,
            schoolDescription=user_form_values.schoolDescription.data
            )
        user_doc.update(add_to_set__education=education)
        return redirect(url_for('mod_profile.update_education'))




@mod_profile.route('/create-education', methods=['POST', 'GET'])
@login_required
def create_education():
    user_form = RegisterForm()
    if request.method == 'GET' and current_user.is_authenticated():
        return render_template(
            'home/create_education.html',
            form=user_form
        )
    elif request.method == 'POST':
        user_doc = User.objects.get(email=current_user.email)
        education = Education(
            school=user_form.school.data,
            fieldOfStudy=user_form.fieldOfStudy.data,
            schoolDegree=user_form.schoolDegree.data,
            startDateSchool=user_form.startDateSchool.data,
            endDateSchool=user_form.endDateSchool.data,
            schoolDescription=user_form.schoolDescription.data
            )
        user_doc.update(push__education=education)
        return redirect(url_for('mod_profile.profile'))
    else:
        return render_template('home/index.html')



@mod_profile.route('/update-experience', methods=['POST', 'GET'])
@login_required
def update_experience():
    user_doc = User.objects.get(email=current_user.email)
    experience = user_doc['experience']
    user_form = RegisterForm()

    if request.method == "GET":
        if current_user.is_authenticated():
            if experience.exp_id():
                if experience:
                    user_form.companyName.data = experience['companyName']
                    user_form.startDateWork.data = experience['startDateWork']
                    user_form.endDateWork.data = experience['endDateWork']
                    user_form.workPosition.data = experience['workPosition']
                    user_form.companyLocation.data = experience['companyLocation']
                    user_form.experienceDescription.data = experience['experienceDescription']
                    return render_template(
                        'home/update_experience.html',
                        form=user_form,
                        action=url_for('mod_profile.update_experience'),
                        display_pass_field=True
                    )
            else:
                return render_template(
                    'home/update_experience.html',
                    form=user_form,
                    action=url_for('mod_profile.update_experience'),
                    display_pass_field=True
                )
        else:
            return render_template('home/index.html')
    elif request.method == "POST":
        experience = Experience(
            companyName=user_form.companyName.data,
            startDateWork=user_form.startDateWork.data,
            endDateWork=user_form.endDateWork.data,
            workPosition=user_form.workPosition.data,
            companyLocation=user_form.companyLocation.data,
            experienceDescription=user_form.experienceDescription.data
        )

        user_doc.update(set__experience=experience)
        return redirect(url_for('mod_profile.update_summary'))

@mod_profile.route('/create-experience', methods=['POST', 'GET'])
@login_required
def create_experience():
    user_form = RegisterForm()
    if request.method == 'GET' and current_user.is_authenticated():
        return render_template(
            'home/create_experience.html',
            form=user_form
        )
    elif request.method == 'POST':
        user_doc = User.objects.get(email=current_user.email)
        experience = Experience(
            _id=ObjectId(),
            companyName=user_form.companyName.data,
            startDateWork=user_form.startDateWork.data,
            endDateWork=user_form.endDateWork.data,
            workPosition=user_form.workPosition.data,
            companyLocation=user_form.companyLocation.data,
            experienceDescription=user_form.experienceDescription.data
        )

        user_doc.update(push__experience=experience)
        return redirect(url_for('mod_profile.profile'))
    else:
        return render_template('home/index.html')



@mod_profile.route('/update-summary', methods=['POST', 'GET'])
@login_required
def update_summary():
    user_doc = User.objects.get(email=current_user.email)
    user_form = RegisterForm()

    if request.method == "GET":
        if current_user.is_authenticated():
            user_form.cvSummary.data = user_doc['cvSummary']
            return render_template(
                'home/update_summary.html',
                form=user_form,
                action=url_for('mod_profile.update_summary'),
                display_pass_field=True
            )
        else:
            return render_template('home/index.html')
    elif request.method == "POST":
        user_doc.update(
            set__cvSummary=user_form.cvSummary.data
        )
        return redirect(url_for('mod_profile.profile'))
