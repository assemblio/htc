from flask import Blueprint, render_template, request, redirect
from flask.ext.security import roles_required, login_required, current_user
from flask.ext.mongoengine import DoesNotExist
from .form import CreateJob
from .model import Job
from app.modules.public.mod_authentication.user_registration.model import User
from bson import ObjectId
# Define the blueprint:
mod_apply_for_job = Blueprint('mod_apply_for_job', __name__)

# Set the route and accepted methods

@mod_apply_for_job.route('/jobs')
def index():
    jobs = Job.objects()
    return render_template('applications/jobs.html', jobs=jobs)


@mod_apply_for_job.route('/job/<string:job_id>')
def job(job_id):
    jobs = Job.objects.get(id=ObjectId(job_id))
    return render_template('applications/jobs-single.html', jobs=jobs)

@mod_apply_for_job.route('/job/apply/<string:job_id>')
@login_required
def apply_for_job(job_id):
    try:
        job = Job.objects.get(id=ObjectId(job_id))
        Job.objects.get(applicants=ObjectId(current_user.id))
    except DoesNotExist:
        Job.objects.get(id=ObjectId(job_id)).update(push__applicants=current_user.id)
        User.objects.get(id=ObjectId(current_user.id)).update(push__jobs_applied=ObjectId(job_id))
        return "Succesfully applied for this job."
    return "You already applied for this job."

@mod_apply_for_job.route('/create-job', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateJob(request.form)
    job = Job(
        title=form.title.data,
        date=form.date.data,
        location=form.location.data,
        description=form.description.data,
        requirements=form.requirements.data
    )
    if form.validate_on_submit():
        job.save()
    # user_datastore.add_role_to_user(user, "User")
        return redirect('/jobs')
    return render_template('applications/createJob.html', form=form)

