# Minimalist Workout Journal
I love stats of my workouts, but I hate spending time meticulously
filling them in by hand to then add them to some sort of webpage again later.

I figured it could be written more succintly, since my workouts don't change every time, and it usually follows a pattern.
Most of the time I stick to the same exercises as well.

So, there has to be a better way?

## Usage

Input to this script would look something like this `s,1x5+27` and is short for `s(quats),1(set)x5(reps)+27(kg)`.

You can then expand this out to a more complete workout like this `s,1x5+27;p,17;c,2x5'1x8` where `'` separates
your sets if they are of different length or have different weight.

You can add your own shortcuts for exercise-names in the mapping-file.

### Separators
* `,` - `exercise-name,more` - Splits exercise shortcuts from the rest
* `;` - `exercise+more;exercise-more` - Splits each exercise from each other
* `'` - `1x5'2x3` - Splits different length sets from each other
* `+/-` - `1x5+25 2x3-22` - Separates sets from the weight for each set. (negative for assisted sets)


## Backend
The project currently uses [Wger](https://github.com/wger-project/wger) as a backend. You can make a user at 
[https://wger.de](https://wger.de), and hook up your API-token to this application.

This will allow for owning the data yourself, and make it possible to generate nice visualizations of progress further
down the road.
