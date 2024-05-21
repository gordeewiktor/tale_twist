# app/blueprints/main.py
from flask import Blueprint, render_template
from app.models import Story, Segment  # Adjust the import statement like this
from sqlalchemy.orm import joinedload

main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/')
def home():
    stories_with_first_segment = []
    all_stories = Story.query.options(joinedload(Story.author)).all()
    for story in all_stories:
        first_segment = Segment.query.filter_by(story_id=story.id).order_by(Segment.order.asc()).first()
        if first_segment:
            first_segment_id = first_segment.id
            stories_with_first_segment.append((story, first_segment_id))
        else:
            # Handle the case where there are no segments
            stories_with_first_segment.append((story, None))
    
    return render_template('home.html', stories=stories_with_first_segment)
