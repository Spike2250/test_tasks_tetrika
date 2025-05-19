def appearance(intervals: dict[str, list[int]]) -> int:

    def is_person_in_lesson(timestamp: int, person: str) -> bool:
        person = intervals[person]

        for i in range(len(person) // 2):
            start, stop = person[0 + 2 * i], person[1 + 2 * i]
            if start <= timestamp < stop:
                return True
        return False

    all_time = 0
    lesson_start, lesson_end = intervals['lesson'][0], intervals['lesson'][1]

    for time in range(lesson_start, lesson_end):
        if all((
                is_person_in_lesson(time, 'pupil'),
                is_person_in_lesson(time, 'tutor'),
        )):
            all_time += 1

    return all_time
