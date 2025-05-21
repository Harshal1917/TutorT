from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required # We'll want to protect admin routes
from app.admin import bp # The admin blueprint we created
from app.admin.forms import SubjectForm # Our new form
from app.models import Subject # The Subject model
from app.forms import ResourceForm #// Make sure to import ResourceForm
from app.models import Subject, Resource #// Make sure to import Subject and Resource
from app import db #// Import db

@bp.route('/add_subject', methods=['GET', 'POST'])
@login_required # Ensures only logged-in users can access this page
def add_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        # Check if subject already exists
        existing_subject = Subject.query.filter_by(name=form.name.data).first()
        if existing_subject:
            flash('A subject with this name already exists.', 'warning')
            return render_template('admin/add_subject.html', title='Add New Subject', form=form)

        subject = Subject(name=form.name.data, 
                          description=form.description.data, 
                          category=form.category.data)
        db.session.add(subject)
        db.session.commit()
        flash('New subject added successfully!', 'success')
        return redirect(url_for('admin.list_subjects')) # We'll create list_subjects next
    return render_template('admin/add_subject.html', title='Add New Subject', form=form)

# Placeholder for listing subjects - we will build this out properly
@bp.route('/subjects')
@login_required
def list_subjects():
    subjects = Subject.query.order_by(Subject.name).all()
    return render_template('admin/list_subjects.html', title='Manage Subjects', subjects=subjects)

# Basic admin dashboard (optional, can be expanded later)
@bp.route('/') #  will be /admin/
@login_required
def dashboard():
    return render_template('admin/dashboard.html', title='Admin Dashboard')


@bp.route('/edit_subject/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def edit_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    form = SubjectForm(obj=subject)
    
    if form.validate_on_submit():
        # Check for name conflicts excluding current subject
        existing = Subject.query.filter(
            Subject.name == form.name.data,
            Subject.id != subject_id
        ).first()
        
        if existing:
            flash('Subject name already exists', 'danger')
            return redirect(url_for('admin.edit_subject', subject_id=subject_id))
        
        form.populate_obj(subject)
        db.session.commit()
        flash('Subject updated successfully', 'success')
        return redirect(url_for('admin.list_subjects'))
    
    return render_template('admin/edit_subject.html', 
                         title='Edit Subject',
                         form=form,
                         subject=subject)


@bp.route('/subject/<int:subject_id>/add_resource', methods=['GET', 'POST']) # Changed admin_bp to bp
@login_required
def add_resource(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    form = ResourceForm()
    if form.validate_on_submit():
        # Create a new Resource instance
        new_resource = Resource(
            title=form.title.data,
            resource_type=form.resource_type.data,
            content=form.content.data,
            url=form.url.data,
            subject_id=subject.id
        )
        db.session.add(new_resource)
        db.session.commit()
        flash('New resource added successfully!', 'success')
        # Redirect to a page showing resources for this subject (we'll create this later)
        return redirect(url_for('admin.list_resources_for_subject', subject_id=subject.id)) 
    return render_template('admin/add_resource.html', title='Add New Resource', 
                           form=form, subject=subject)

@bp.route('/subject/<int:subject_id>/resources', methods=['GET'])
@login_required
def list_resources_for_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    # Assuming your Resource model has a relationship back to Subject
    # and a way to get resources for a subject, e.g., subject.resources
    # If not, you might query like: Resource.query.filter_by(subject_id=subject.id).all()
    resources = subject.resources # Or Resource.query.filter_by(subject_id=subject.id).all()
    return render_template('admin/list_resources_for_subject.html', 
                           title=f"Resources for {subject.name}", 
                           subject=subject, 
                           resources=resources)
