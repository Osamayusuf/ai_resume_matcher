def calculate_match(user_skills, job_skills):
    user_skills = set(user_skills.lower().split(","))
    job_skills = set(job_skills.lower().split(","))

    matched = user_skills.intersection(job_skills)

    if len(job_skills) == 0:
        return 0

    score = (len(matched) / len(job_skills)) * 100
    return round(score)
def get_missing_skills(user_skills, job_skills):
    user_skills = set(user_skills.lower().split(","))
    job_skills = set(job_skills.lower().split(","))

    missing = job_skills - user_skills
    return list(missing)