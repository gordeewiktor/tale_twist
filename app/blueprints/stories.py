from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.models import db, Story, Segment, Choice
from app.forms import CreateStoryForm as StoryForm, SegmentForm
from sqlalchemy.orm import joinedload

stories_bp = Blueprint('stories', __name__, url_prefix='/stories')

@stories_bp.route('/')
def index():
    stories_with_first_segment = []
    all_stories = Story.query.options(joinedload(Story.author)).all()
    for story in all_stories:
        first_segment = Segment.query.filter_by(story_id=story.id).order_by(Segment.order.asc()).first()
        first_segment_id = first_segment.id if first_segment else None
        stories_with_first_segment.append((story, first_segment_id))
    
    return render_template('stories.html', stories=stories_with_first_segment)

@stories_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_story():
    form = StoryForm()
    if form.validate_on_submit():
        new_story = Story(title=form.title.data, description=form.description.data, genre=form.genre.data, author=current_user)
        db.session.add(new_story)
        db.session.commit()
        flash('Story created successfully!', 'success')
        return redirect(url_for('stories.index'))
    return render_template('create_story.html', form=form)

@stories_bp.route('/<int:story_id>/manage', methods=['GET'])
@login_required
def manage_story(story_id):
    story = Story.query.get_or_404(story_id)
    if current_user != story.author:
        flash('You can only manage your own stories.', 'danger')
        return redirect(url_for('stories.index'))

    segments = Segment.query.filter_by(story_id=story_id).all()
    
    for segment in segments:
        print(f"Segment {segment.id}: {segment.title}")
        if segment.choices:
            for choice in segment.choices:
                print(f"  Choice {choice.id}: {choice.text} -> {choice.next_segment_id}")
        else:
            print(f"  Segment {segment.id} has no choices")

    # Create a dummy form object to use for CSRF token generation
    from flask_wtf import FlaskForm
    class DummyForm(FlaskForm):
        pass
    form = DummyForm()

    return render_template('manage_story.html', story=story, segments=segments, form=form)



@stories_bp.route('/read/<int:story_id>/<int:segment_id>')
def read_story(story_id, segment_id):
    story = Story.query.get_or_404(story_id)
    segment = Segment.query.filter_by(id=segment_id, story_id=story_id).first()

    if not segment:
        flash('The requested segment does not belong to this story.', 'danger')
        return redirect(url_for('stories.index'))  # Redirect them to a safe page

    # Check if the current segment is the first segment
    first_segment = Segment.query.filter_by(story_id=story_id).order_by(Segment.order.asc()).first()
    segment.is_first = (segment.id == first_segment.id)

    # Fetch choices associated with the current segment
    choices = Choice.query.filter_by(segment_id=segment.id).all()
    print(f"Choices found: {len(choices)}")

    # Render the template with the necessary context
    return render_template('read_story.html', story=story, segment=segment, choices=choices)

@stories_bp.route('/<int:story_id>/segments/add', methods=['GET', 'POST'])
@login_required
def add_segment(story_id):
    story = Story.query.get_or_404(story_id)
    if current_user != story.author:
        flash('You can only add segments to your own stories.', 'danger')
        return redirect(url_for('stories.index'))

    form = SegmentForm()
    if form.validate_on_submit():
        new_segment = Segment(story_id=story_id, title=form.title.data, content=form.content.data)
        db.session.add(new_segment)
        db.session.commit()

        # Handle choices for the new segment
        if form.choice_text_1.data:
            next_segment_id_1 = int(form.next_segment_id_1.data) if form.next_segment_id_1.data and form.next_segment_id_1.data != 'None' else None
            new_choice1 = Choice(segment_id=new_segment.id, text=form.choice_text_1.data, next_segment_id=next_segment_id_1)
            db.session.add(new_choice1)

        if form.choice_text_2.data:
            next_segment_id_2 = int(form.next_segment_id_2.data) if form.next_segment_id_2.data and form.next_segment_id_2.data != 'None' else None
            new_choice2 = Choice(segment_id=new_segment.id, text=form.choice_text_2.data, next_segment_id=next_segment_id_2)
            db.session.add(new_choice2)

        db.session.commit()

        flash('New segment added successfully!', 'success')
        return redirect(url_for('stories.read_story', story_id=story_id, segment_id=new_segment.id))

    return render_template('manage_segment.html', form=form, story=story, segment=None)



@stories_bp.route('/<int:story_id>/segments/edit/<int:segment_id>', methods=['GET', 'POST'])
@login_required
def edit_segment(story_id, segment_id):
    story = Story.query.get_or_404(story_id)
    segment = Segment.query.get_or_404(segment_id)
    if current_user != story.author or segment.story_id != story_id:
        flash('You are not authorized to edit this segment.', 'danger')
        return redirect(url_for('stories.index'))

    form = SegmentForm(obj=segment)
    form.set_choices(Segment.query.filter(Segment.story_id == story_id, Segment.id != segment_id).all(), segment_id)

    # Load existing choices
    choices = Choice.query.filter_by(segment_id=segment_id).all()

    if form.validate_on_submit():
        form.populate_obj(segment)
        
        # Update or create choices
        if form.choice_text_1.data:
            if len(choices) > 0:
                choices[0].text = form.choice_text_1.data
                choices[0].next_segment_id = int(form.next_segment_id_1.data) if form.next_segment_id_1.data != 'None' else None
            else:
                new_choice1 = Choice(segment_id=segment_id, text=form.choice_text_1.data, next_segment_id=int(form.next_segment_id_1.data) if form.next_segment_id_1.data != 'None' else None)
                db.session.add(new_choice1)
        elif len(choices) > 0:
            db.session.delete(choices[0])

        if form.choice_text_2.data:
            if len(choices) > 1:
                choices[1].text = form.choice_text_2.data
                choices[1].next_segment_id = int(form.next_segment_id_2.data) if form.next_segment_id_2.data != 'None' else None
            else:
                new_choice2 = Choice(segment_id=segment_id, text=form.choice_text_2.data, next_segment_id=int(form.next_segment_id_2.data) if form.next_segment_id_2.data != 'None' else None)
                db.session.add(new_choice2)
        elif len(choices) > 1:
            db.session.delete(choices[1])

        db.session.commit()
        flash('Segment updated successfully!', 'success')
        return redirect(url_for('stories.read_story', story_id=story_id, segment_id=segment.id))

    # Prepopulate form with choice data if any
    if choices:
        if len(choices) > 0:
            form.choice_text_1.data = choices[0].text
            form.next_segment_id_1.data = str(choices[0].next_segment_id) if choices[0].next_segment_id else 'None'
        if len(choices) > 1:
            form.choice_text_2.data = choices[1].text
            form.next_segment_id_2.data = str(choices[1].next_segment_id) if choices[1].next_segment_id else 'None'

    return render_template('manage_segment.html', form=form, story=story, segment=segment)




@stories_bp.route('/<int:story_id>/segments/delete/<int:segment_id>', methods=['POST'])
@login_required
def delete_segment(story_id, segment_id):
    story = Story.query.get_or_404(story_id)
    segment = Segment.query.get_or_404(segment_id)
    if current_user != story.author or segment.story_id != story_id:
        flash('You are not authorized to delete this segment.', 'danger')
        return redirect(url_for('stories.manage_story', story_id=story_id))

    db.session.delete(segment)
    db.session.commit()
    flash('Segment deleted successfully!', 'success')
    return redirect(url_for('stories.manage_story', story_id=story_id))

# Add this route to handle story deletion
@stories_bp.route('/delete/<int:story_id>', methods=['POST'])
@login_required
def delete_story(story_id):
    story = Story.query.get_or_404(story_id)
    if current_user != story.author:
        flash('You are not authorized to delete this story.', 'danger')
        return redirect(url_for('stories.index'))
    
    # Delete all segments and choices related to this story
    segments = Segment.query.filter_by(story_id=story.id).all()
    for segment in segments:
        choices = Choice.query.filter_by(segment_id=segment.id).all()
        for choice in choices:
            db.session.delete(choice)
        db.session.delete(segment)
    
    db.session.delete(story)
    db.session.commit()
    flash('Story and all its segments have been deleted.', 'success')
    return redirect(url_for('stories.index'))



# Handling 404 and 500 errors at the blueprint level
@stories_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@stories_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
