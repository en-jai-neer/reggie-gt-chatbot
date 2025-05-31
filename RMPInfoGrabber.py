from ratemyprofessor import get_school_by_name, get_professor_by_school_and_name
import ratemyprofessor

def fetch_professor_data(school_name, last_name, full_name):
    try:
        # Step 1: Get the school object
        school = ratemyprofessor.get_school_by_name(school_name)
        if not school:
            print(f"School '{school_name}' not found.")
            return
        
        # Step 2: Search for professors by last name
        print(f"Searching for professors with the last name '{last_name}' at '{school_name}'...")
        professors = ratemyprofessor.get_professors_by_school_and_name(school, last_name)

        if not professors:
            print(f"No professors found with the last name '{last_name}' at '{school_name}'.")
            return
        
        # Print all professors returned
        print(f"Professors returned with the last name '{last_name}':")
        for prof in professors:
            print(f"- {prof.name} (Department: {prof.department})")

        # Step 3: Look for an exact match with the full name
        print(f"Looking for an exact match with the name '{full_name}'...")
        for prof in professors:
            r = ""
            if prof.name.lower() == full_name.lower():
                r += (f"Match found: {prof.name} ")
                r += ("Professor Details: ")
                r += ("%s works in the %s Department of %s. " % (prof.name, prof.department, prof.school.name))
                r += ("Rating: %s / 5.0. " % prof.rating)
                r += ("Difficulty: %s / 5.0. " % prof.difficulty)
                r += ("Total Ratings: %s. " % prof.num_ratings)
                if prof.would_take_again is not None:
                    r += (("Would Take Again: %s." % round(prof.would_take_again, 1)) + '%')
                else:
                    r += ("Would Take Again: N/A.")
                return r
        # Step 4: If no match is found
        return f"Unable to find information regarding {full_name}."
    except Exception as e:
        return ""

if __name__ == "__main__":
    school_name = "Georgia Institute of Technology"
    last_name = "Smith"
    full_name = "John Smith"
    fetch_professor_data(school_name, last_name, full_name)
