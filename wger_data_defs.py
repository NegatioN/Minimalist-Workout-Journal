
#TODO add a way to say something about how the workout went to graph form better later.
def create_workout_session(session_date, workout_id):
    return {
        "date": str(session_date),
        "notes": "",
        "impression": "1",
        "time_start": None,
        "time_end": None,
        "workout": workout_id
    }


def create_set_object(exercise_id, reps, weight, date, workout_id=121764):
    return {"reps": reps,
            "weight": weight,
            "exercise": exercise_id,
            "workout": workout_id,
            "repetition_unit": 1,
            "weight_unit": 1,
            "date": str(date)}


def create_workout(comment=""):
    return {"comment": comment}
