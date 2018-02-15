[![Build Status](https://travis-ci.org/NegatioN/Minimalist-Workout-Journal.svg)](https://travis-ci.org/NegatioN/Minimalist-Workout-Journal)
# Minimalist Workout Journal
I love stats of my workouts, but I hate spending time meticulously
filling them in by hand to then add them to some sort of webpage again later.

I figured it could be written more succintly, since my workouts don't change every time, and it usually follows a pattern.
Most of the time I stick to the same exercises as well.

So, there has to be a better way?

## Usage

Input to this script would look something like this `s,1*5+27` and is short for `s(quats),1(set)*5(reps)+27(kg)`.

You can then expand this out to a more complete workout like this `s,1*5+27;p,17;c,2*5'1x8` where `'` separates
your sets if they are of different length or have different weight.

You can add your own shortcuts for exercise-names in the mapping-file.

### Separators
* `*` - `1*5` - Indicates how many reps were done for a set.
* `,` - `exercise-name,more` - Splits exercise shortcuts from the rest
* `;` - `exercise+more;exercise-more` - Splits each exercise from each other
* `'` - `1*5'2x3` - Splits different length sets from each other
* `+/-` - `1*5+25 2*3-22` - Separates sets from the weight for each set. (negative for assisted sets)
