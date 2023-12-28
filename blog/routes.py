# blog/routes.py

from flask import render_template, request, flash, url_for, redirect, session
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm
from blog.forms import LoginForm
import functools


def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args, **kwargs):
        if session.get('logged_in'):
            return view_func(*args, **kwargs)
        return redirect(url_for('login', next=request.path))

    return check_permissions


@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)


@app.route("/post/", methods=["GET", "POST"])
@app.route("/post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_or_create_entry(entry_id=None):
    form = EntryForm()
    errors = None
    entry = Entry.query.get_or_404(entry_id) if entry_id else None

    if entry and request.method == 'GET':
        # Pre-fill the form for editing an existing entry
        form = EntryForm(obj=entry)

    if form.validate_on_submit():
        if not entry:
            # Create a new entry
            entry = Entry(
                title=form.title.data,
                body=form.body.data,
                is_published=form.is_published.data
            )
            db.session.add(entry)
            flash('Entry added!', 'success')
        else:
            # Update an existing entry
            form.populate_obj(entry)
            flash('Entry updated!', 'success')

        db.session.commit()
    else:
        errors = form.errors

    return render_template("entry_form.html", form=form, errors=errors, entry_id=entry_id)


@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('index'))
        else:
            # errors = form.errors
            flash('Invalid username or password', 'error')  # Flash an error message
            return redirect(url_for('login'))  # Redirect back to the login page

    return render_template("login_form.html", form=form, errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You are now logged out.', 'success')
    return redirect(url_for('index'))


@app.route("/drafts/", methods=['GET'])
@login_required
def list_drafts():
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
    return render_template("drafts.html", drafts=drafts)


@app.route("/delete/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id=None):
    if request.method == 'POST':
        entry = Entry.query.get_or_404(entry_id) if entry_id else None

        if entry:
            db.session.delete(entry)
            db.session.commit()
            flash('Entry deleted successfully!', 'success')
        else:
            flash('Entry not found or already deleted.', 'error')

    return redirect(url_for('index'))
