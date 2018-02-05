def create_workout(session_date, exercises):
    return {
        "date": str(session_date),
        "comment": "",
        "session_rating": "1",
        "exercises": exercises
    }

def create_exercise(exercise_id, sets):
    return {
        "exercise_id": exercise_id,
        "sets": sets
    }

def create_set_object(reps, weight):
    return {"reps": reps,
            "weight": weight,
            "repetition_unit": 1,
            "weight_unit": 1}
