import pandas as pd

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
            "weight_unit": 'kg'}


def json_workout_to_df(dict_style_workout):
    date = dict_style_workout['date']
    exr_id, amount, weight, denom = [], [], [], []
    # construct columns
    for exercise in dict_style_workout['exercises']:
        for set in exercise['sets']:
            exr_id.append(exercise['exercise_id'])
            amount.append(set['reps'])
            weight.append(set['weight'])
            denom.append(set['weight_unit'])

    return pd.DataFrame(data={'exercise': exr_id,
                           'amount': amount,
                           'weight': weight,
                           'denominator': denom,
                           'date': [date for x in range(len(exr_id))]})


def join_workout_dfs(master_df, input_df, save_path):
    df = pd.concat([master_df, input_df])
    df.to_csv(save_path, index=False)
    return df
