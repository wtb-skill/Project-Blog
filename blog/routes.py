# blog/routes.py

from flask import render_template, request, flash
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm


@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)


@app.route("/post/", methods=["GET", "POST"])
@app.route("/post/<int:entry_id>", methods=["GET", "POST"])
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
