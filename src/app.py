"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
    ,
    "Soccer Team": {
        "description": "Competitive soccer team practicing skills and playing matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["alex@mergington.edu", "nina@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Pickup games and skill development for basketball enthusiasts",
        "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["tyler@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore drawing, painting, and mixed media projects",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["lily@mergington.edu", "sam@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting, stagecraft, and producing school plays",
        "schedule": "Thursdays, 3:30 PM - 6:00 PM",
        "max_participants": 30,
        "participants": ["maya@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments and science fair project development",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["liam@mergington.edu", "zoe@mergington.edu"]
    },
    "Debate Team": {
        "description": "Practice public speaking and competitive debating",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["noah@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Normalize email
    email_norm = email.strip().lower()

    # Prevent duplicate signup
    if email_norm in (e.lower() for e in activity["participants"]):
        raise HTTPException(status_code=400, detail="Already signed up")

    # Enforce max capacity
    if len(activity["participants"]) >= activity.get("max_participants", 0):
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def remove_participant(activity_name: str, email: str):
    """Remove a participant from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    email_norm = email.strip().lower()

    # Find participant (case-insensitive) and remove
    for i, p in enumerate(activity.get("participants", [])):
        if p.strip().lower() == email_norm:
            activity["participants"].pop(i)
            return {"message": f"Removed {email_norm} from {activity_name}"}

    raise HTTPException(status_code=404, detail="Participant not found")
