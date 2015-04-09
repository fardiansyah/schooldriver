# never import * except test data (because who cares about clean tests)
from ecwsp.sis.models import *
from ecwsp.attendance.models import *
from ecwsp.admissions.models import *
from ecwsp.grades.models import *
from ecwsp.gradebook.models import *
from ecwsp.schedule.models import *
from ecwsp.benchmarks.models import *
from django.contrib.auth.models import User, Group, Permission

import random
import string
import logging
import datetime

class SisGUIData(object):
    """ Put data creation code here.
    """
    def create_all(self):
        """ This will populate all sample data """
        self.create_basics()
        self.create_admissions_choice_data()

    def create_required(self):
        """ A place for 100% required data """
        self.normal_type = CourseType.build_default()

    def create_basics(self):
        """ 
        A more complex school than sample_data.py. Whereas that file is meant
        to run faster and work with unit tests, this is more about demoing the
        software as well as doing front-end work, be it creating new features
        or debugging existing ones.

        If you debug issues and find that you needed to enter a bunch of data
        so that you could duplicate the problem locally, think about putting
        said data in here so it'll be around when you need it later.

        Depends on create_required
        """
        # Run dependencies first
        self.create_required()

        # Add graduating classes, birthdays, etc. that won't get outdated
        now = datetime.datetime.now()
        
        graduated_year = now.year - 1
        senior_year = now.year
        junior_year = now.year + 1
        sophomore_year = now.year + 2
        freshman_year = now.year + 3

        self.class_year0 = ClassYear.objects.create(
            year=graduated_year,
            full_name="Class of " + str(graduated_year))
        self.class_year1 = ClassYear.objects.create(
            year=senior_year,
            full_name="Class of " + str(senior_year))
        self.class_year2 = ClassYear.objects.create(
            year=junior_year,
            full_name="Class of " + str(junior_year))
        self.class_year3 = ClassYear.objects.create(
            year=sophomore_year,
            full_name="Class of " + str(sophomore_year))
        self.class_year4 = ClassYear.objects.create(
            year=freshman_year,
            full_name="Class of " + str(freshman_year))

        # Populate grade levels
        GradeLevel.objects.bulk_create([
            GradeLevel(id=9, name="Freshman"),
            GradeLevel(id=10, name="Sophomore"),
            GradeLevel(id=11, name="Junior"),
            GradeLevel(id=12, name="Senior"),
        ])

        # Populate some school years based on the current month/year
        school_year_base = now.year
        # If in 2015 and not yet August, active year will be 2014-2015. 
        # After August 1 it'll be 2015-2016
        if now.month < 8:
            school_year_base = now.year - 1

        current_school_year = str(school_year_base)+"-"+str(school_year_base+1)

        SchoolYear.objects.bulk_create([
            SchoolYear(
                name=str(school_year_base+2)+"-"+str(school_year_base+3),
                start_date=datetime.date(school_year_base+2,8,1),
                end_date=datetime.date(school_year_base + 3,7,31)),
            SchoolYear(
                name=str(school_year_base+1)+"-"+str(school_year_base+2),
                start_date=datetime.date(school_year_base+1,8,1),
                end_date=datetime.date(school_year_base + 2,7,31)),
            SchoolYear(
                name=current_school_year,
                start_date=datetime.date(school_year_base,8,1),
                end_date=datetime.date(school_year_base+1,7,31), 
                active_year=True),
            SchoolYear(
                name=str(school_year_base-1)+"-"+str(school_year_base),
                start_date=datetime.date(school_year_base-1,8,1),
                end_date=datetime.date(school_year_base,7,31)),
            SchoolYear(
                name=str(school_year_base-2)+"-"+str(school_year_base-1),
                start_date=datetime.date(school_year_base-2,8,1),
                end_date=datetime.date(school_year_base-1,7,31)),
            SchoolYear(
                name=str(school_year_base-3)+"-"+str(school_year_base-2),
                start_date=datetime.date(school_year_base-3,8,1),
                end_date=datetime.date(school_year_base-2,7,31)),
        ])
        # Set one archetypal object. If I want a year I will use this
        self.school_year = SchoolYear.objects.get(active_year=True)

        self.cohort1 = Cohort.objects.create(
            name="Class of " + str(senior_year),
            long_name="All Students in Class of " + str(senior_year),
            primary=False)
        self.cohort2 = Cohort.objects.create(
            name="Small Senior Primary",
            long_name="A smaller cohort that will be a primary one too",
            primary=True)

        def random_birthday(class_year):
            day = random.randint(1,28)
            month = random.randint(1,12)
            offset = 0
            # If you're born in September, your birth year will be 1 earlier
            if (month > 8):
                offset = 1
            year = class_year.year - 18 - offset
            return datetime.date(year, month, day)

        def random_ssn():
            first_three = random.randint(100,999)
            middle_two = random.randint(10,99)
            last_four = random.randint(1000,9999)
            ssn_string = str(first_three) + "-" + str(middle_two) + "-" + str(last_four)
            return ssn_string

        # Note bulk does not call save() and other limitations
        # so it's ok to not use bulk
        # Don't change the order, other objects depend on the id being in this order
        self.student   = Student.objects.create(
            first_name="Alex", 
            last_name="Jackson", 
            username="ajackson", 
            sex="M", 
            class_of_year=self.class_year1, 
            bday=random_birthday(self.class_year1), 
            ssn=random_ssn())
        self.student2  = Student.objects.create(
            first_name="Pat", 
            last_name="Williams", 
            username="pwilliams", 
            mname="Logan", 
            sex="F", 
            class_of_year=self.class_year2, 
            bday=random_birthday(self.class_year2), 
            ssn=random_ssn())
        self.student3  = Student.objects.create(
            first_name="Chris", 
            last_name="Robinson", 
            username="crobinson", 
            sex="M", 
            class_of_year=self.class_year3, 
            bday=random_birthday(self.class_year3), 
            ssn=random_ssn())
        # Student 4 will have a lot of information attached to her.
        # Created while working on the Angular view_student template.
        self.student4  = Student.objects.create(
            first_name="Rory", 
            last_name="Robinson", 
            username="rvrst1", 
            mname="Viola",
            sex="F", 
            class_of_year=self.class_year1, 
            bday=random_birthday(self.class_year1), 
            ssn=random_ssn(),
            alert="Watch out for this one!",
            notes="Here is where I'll put some notes about Rory Robinson. " \
                "want to give it more than a sentence so that it'll fill out " \
                "more space. Who knows how long these notes are anyways!",
            )
        # Add Rory to the smaller cohort manually
        StudentCohort.objects.create(
            student=self.student4,
            cohort=self.cohort2)
        # Rory gets two phone numbers! Most students will probably have just
        # one, but if we're iterating through a set it's good to have multiple
        self.student_number1 = StudentNumber.objects.create(
            student=self.student4,
            number="412-523-6347",
            type="C")
        self.student_number2 = StudentNumber.objects.create(
            student=self.student4,
            number="724-835-9460",
            ext="57",
            type="W",
            note="Rory works Saturdays from 8 to 5.")
        # Give Rory two parents with some different fields
        self.student_contact1 = EmergencyContact.objects.create(
            fname="Zoe",
            mname="Iris",
            lname="Robinson",
            relationship_to_student="Mother",
            street="124 8th Ave",
            city="Pittsburgh",
            state="PA",
            zip="15222",
            email="zir_mom@examplemail.com")
        self.student_contact2 = EmergencyContact.objects.create(
            fname="Dante",
            lname="Robinson",
            relationship_to_student="Father",
            street="124 8th Ave",
            city="Pittsburgh",
            state="PA",
            zip="15222",
            email="drobinson@examplemail.com",
            emergency_only=True,
            primary_contact=False)
        # Parents get some phone numbers
        self.student_contact_number1 = EmergencyContactNumber.objects.create(
            contact=self.student_contact1,
            primary=True,
            number="412-214-4124",
            type="H",)
        self.student_contact_number2 = EmergencyContactNumber.objects.create(
            contact=self.student_contact2,
            primary=True,
            number="412-724-7100",
            ext="123",
            note="Working hours 8:30 AM-5:00 PM",
            type="W")
        self.student_contact_number3 = EmergencyContactNumber.objects.create(
            contact=self.student_contact2,
            primary=False,
            number="412-814-4023",
            type="C")
        # Link parents to Rory
        self.student4.emergency_contacts.add(self.student_contact1)
        self.student4.emergency_contacts.add(self.student_contact2)
        
        # Kept three names attached to variables, but it's time to go full rando here.
        first_names = [
            "Alex", "Pat", "Chris", "Terry", "Ashton", "Ashley", "Cameron", 
            "Casey", "Drew", "Hayden", "Jordan", "Logan", "Micah", "Morgan", 
            "Parker", "Quinn", "Riley", "Sidney", "Taylor", "Devon"
        ]
        # Thanks Wikipedia! 
        # http://en.wikipedia.org/wiki/List_of_most_common_surnames_in_North_America
        last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", 
            "Davis", "Garcia", "Rodriguez", "Wilson", "Martinez", "Anderson", 
            "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson", 
            "Thompson", "White", "Lopez", "Lee", "Gonzalez", "Harris", "Clark",
            "Lewis", "Robinson",  "Walker", "Perez", "Hall", "Young", "Allen", 
            "Sanchez", "Wright", "King",  "Scott", "Green", "Baker", "Adams", 
            "Nelson", "Hill", "Ramirez",  "Campbell", "Mitchell", "Roberts", 
            "Carter", "Phillips", "Evans", "Turner", "Torres", "Parker", 
            "Collins", "Edwards", "Stewart", "Flores", "Morris",  "Nguyen", 
            "Murphy", "Rivera", "Cook", "Rogers", "Morgan", "Peterson", 
            "Cooper", "Reed", "Bailey", "Bell", "Gomez", "Kelly", "Howard", 
            "Ward",  "Cox", "Diaz", "Richardson", "Wood", "Watson", "Brooks", 
            "Bennett", "Gray", "James", "Reyes", "Cruz", "Hughes", "Price", 
            "Myers", "Long", "Foster",  "Sanders", "Ross", "Morales", "Powell",
            "Sullivan", "Russell", "Ortiz",  "Jenkins", "Gutierrez", "Perry", 
            "Butler", "Barnes", "Fisher"
        ]

        random_usernames = []

        for i in xrange(150):
            random_first = random.choice(first_names)
            
            random_middle = random.choice(first_names)
            # People don't have the same first and middle names!
            while random_middle == random_first:
                random_middle = random.choice(first_names)

            random_last = random.choice(last_names)
            
            random_class_year = random.choice([self.class_year1, self.class_year2, 
                self.class_year3, self.class_year4])
            
            # Username generation: initials, 'st' for student, then a unique number
            not_random_username = random_first[0].lower() + \
                random_middle[0].lower() + random_last[0].lower() + "st"

            number = 1
            while not_random_username + str(number) in random_usernames:
                number += 1

            not_random_username = not_random_username + str(number)

            random_usernames.append(not_random_username)

            Student.objects.create(
                first_name=random_first,
                last_name=random_last,
                username=not_random_username,
                mname=random_middle,
                sex=random.choice("MF"),
                class_of_year=random_class_year,
                bday=random_birthday(random_class_year),
                ssn=random_ssn()
            )

        # Let's put all the seniors into our senior cohort
        self.senior_students = Student.objects.filter(
            class_of_year=self.class_year1)

        for student in self.senior_students:
            StudentCohort.objects.create(
                student=student, 
                cohort=self.cohort1)

        MarkingPeriod.objects.bulk_create([
            MarkingPeriod(
                name="Trimester 1 "+current_school_year,
                shortname="Tri 1",
                start_date=datetime.date(school_year_base,8,1),
                end_date=datetime.date(school_year_base,11,30),
                school_year=self.school_year,
                monday=True,
                friday=True
            ),
            MarkingPeriod(
                name="Trimester 2 "+current_school_year,
                shortname="Tri 2",
                start_date=datetime.date(school_year_base,12,1),
                end_date=datetime.date(school_year_base+1,2,28),
                school_year=self.school_year,
                monday=True,
                friday=True
            ),
            MarkingPeriod(
                name="Trimester 3 "+current_school_year,
                shortname="Tri 3",
                start_date=datetime.date(school_year_base+1,3,1),
                end_date=datetime.date(school_year_base+1,5,31),
                school_year=self.school_year,
                monday=True,
                friday=True
            ),
            MarkingPeriod(
                name="Summer Session "+current_school_year,
                shortname="Summer",
                start_date=datetime.date(school_year_base+1,6,1),
                end_date=datetime.date(school_year_base+1,7,31),
                school_year=self.school_year,
                monday=True,
                friday=True
            ),
        ])
        self.marking_period = MarkingPeriod.objects.get(shortname="Tri 1")
        self.marking_period2 = MarkingPeriod.objects.get(shortname="Tri 2")
        self.marking_period3 = MarkingPeriod.objects.get(shortname="Tri 3")

        # Add teacher group with some permissions
        teacher_group = Group.objects.create(name="teacher")

        teacher_perm1 = Permission.objects.get(codename="view_student")
        teacher_perm2 = Permission.objects.get(codename="take_studentattendance")
        teacher_perm3 = Permission.objects.get(codename="change_own_grade")
        teacher_perm4 = Permission.objects.get(codename="add_referralform")

        teacher_group.permissions.add(teacher_perm1)
        teacher_group.permissions.add(teacher_perm2)
        teacher_group.permissions.add(teacher_perm3)
        teacher_group.permissions.add(teacher_perm4)

        # Add some teachers and other users
        self.teacher1 = self.faculty = Faculty.objects.create(
            username="dburke", 
            first_name="David", 
            last_name="Burke", 
            teacher=True)

        self.teacher2 = Faculty.objects.create(
            username="lbritner", 
            first_name="Louis", 
            last_name="Britner", 
            teacher=True, 
            is_staff=True)
        # self.teacher2.groups.add(teacher_group)
        self.teacher2.set_password('aa')
        self.teacher2.save()

        aa = Faculty.objects.create(
            username="aa", 
            first_name="aa", 
            is_superuser=True, 
            is_staff=True)
        aa.set_password('aa')
        aa.save()

        admin = Faculty.objects.create(
            username="admin", 
            first_name="admin", 
            is_superuser=True, 
            is_staff=True)
        admin.set_password('admin')
        admin.save()

        Course.objects.bulk_create([
            Course(fullname="Math 101", shortname="Math101", credits=3, graded=True),
            Course(fullname="History 101", shortname="Hist101", credits=3, graded=True),
            Course(fullname="Homeroom FX 2011", shortname="FX1", homeroom=True, credits=1),
            Course(fullname="Homeroom FX 2012", shortname="FX2", homeroom=True, credits=1),
        ])
        self.course = Course.objects.get(fullname="Math 101")
        self.course2 = Course.objects.get(fullname="History 101")

        CourseSection.objects.bulk_create([
            CourseSection(course_id=self.course.id, name="Math A"),
            CourseSection(course_id=self.course.id, name="Math B"),
            CourseSection(course_id=self.course.id, name="Math C"),
            CourseSection(course_id=self.course2.id, name="History A"),
            CourseSection(course_id=self.course2.id, name="History 1 MP only"),
        ])
        self.course_section = self.course_section1 = CourseSection.objects.get(name="Math A")
        self.course_section2 = CourseSection.objects.get(name="Math B")
        self.course_section3 = CourseSection.objects.get(name="History A")
        self.course_section4 = CourseSection.objects.get(name="History 1 MP only")
        self.course_section5 = CourseSection.objects.get(name="Math C")

        Period.objects.bulk_create([
            Period(name="Homeroom (M)", start_time=datetime.time(8), end_time=datetime.time(8, 50)),
            Period(name="First Period", start_time=datetime.time(9), end_time=datetime.time(9, 50)),
            Period(name="Second Period", start_time=datetime.time(10), end_time=datetime.time(10, 50)),
        ])
        self.period = Period.objects.get(name="Homeroom (M)")

        CourseMeet.objects.bulk_create([
            CourseMeet(course_section_id=self.course_section.id, period=self.period, day="1"),
            CourseMeet(course_section_id=self.course_section3.id, period=self.period, day="2"),
        ])

        self.course_section1.marking_period.add(self.marking_period)
        self.course_section1.marking_period.add(self.marking_period2)
        self.course_section1.marking_period.add(self.marking_period3)
        self.course_section2.marking_period.add(self.marking_period)
        self.course_section2.marking_period.add(self.marking_period2)
        self.course_section2.marking_period.add(self.marking_period3)
        self.course_section3.marking_period.add(self.marking_period)
        self.course_section3.marking_period.add(self.marking_period2)
        self.course_section3.marking_period.add(self.marking_period3)
        self.course_section4.marking_period.add(self.marking_period)
        self.course_section5.marking_period.add(self.marking_period)
        self.course_section5.marking_period.add(self.marking_period2)
        self.course_section5.marking_period.add(self.marking_period3)

        self.enroll1 = CourseSectionTeacher.objects.create(
            course_section=self.course_section, teacher=self.teacher1)
        self.enroll2 = CourseSectionTeacher.objects.create(
            course_section=self.course_section3, teacher=self.teacher2)
        self.enroll3 = CourseSectionTeacher.objects.create(
            course_section=self.course_section5, teacher=self.teacher2)
        
        self.present = AttendanceStatus.objects.create(
            name="Present", code="P", teacher_selectable=True)
        self.absent = AttendanceStatus.objects.create(
            name="Absent", code="A", teacher_selectable=True, absent=True)
        self.excused = AttendanceStatus.objects.create(
            name="Absent Excused", code="AX", absent=True, excused=True)

        CourseEnrollment.objects.bulk_create([
            CourseEnrollment(user=self.student, course_section=self.course_section),
            CourseEnrollment(user=self.student, course_section=self.course_section2),
            CourseEnrollment(user=self.student, course_section=self.course_section4),
            CourseEnrollment(user=self.student2, course_section=self.course_section),
            CourseEnrollment(user=self.student, course_section=self.course_section3),
            CourseEnrollment(user=self.student2, course_section=self.course_section3),
            CourseEnrollment(user=self.student3, course_section=self.course_section3),
        ])
        self.course_enrollment = CourseEnrollment.objects.all().first()

        # Loading up Math C with the freshmen we created
        self.freshman_students = Student.objects.filter(class_of_year=self.class_year4)

        # Enroll all freshmen until we get to 25
        self.class_size = 25
        self.enroll_counter = 0

        for student in self.freshman_students:
            if self.enroll_counter == self.class_size:
                break
            else:
                CourseEnrollment.objects.create(
                    user=student, course_section=self.course_section5)
                self.enroll_counter += 1

        grade_data = [
            {'student': self.student2, 'section': self.course_section, 'mp': self.marking_period, 'grade': 75},
            {'student': self.student2, 'section': self.course_section, 'mp': self.marking_period2, 'grade': 100},
        ]
        for x in grade_data:
            enrollment = CourseEnrollment.objects.get(
                user=x['student'], course_section=x['section'])
            grade_object, created = Grade.objects.get_or_create(
                enrollment = enrollment,
                marking_period = x['mp']
                )
            grade_object.grade = x['grade']
            grade_object.save()

        self.grade = Grade.objects.all().first()

        """ Gradebook-related things """

        # Assignment Categories for benchmark grading
        AssignmentCategory.objects.bulk_create([
            AssignmentCategory(
                name="Daily Practice",
                display_order=4,
                display_scale=100.00,
                display_symbol="%"),
            AssignmentCategory(
                name="Assignment Completion",
                fixed_points_possible=4.00,
                fixed_granularity=0.50,
                display_order=3),
            AssignmentCategory(
                name="Engagement",
                fixed_points_possible=4.00,
                fixed_granularity=0.50,
                display_order=2),
            AssignmentCategory(
                name="Standards",
                allow_multiple_demonstrations=True,
                demonstration_aggregation_method="Max",
                fixed_points_possible=4.00,
                fixed_granularity=0.50,
                display_order=1),
            AssignmentCategory(
                name="Precision and Accuracy",
                display_in_gradebook=False,
                display_order=5),
        ])

        # Assignment Types for benchmark grading
        AssignmentType.objects.bulk_create([
            AssignmentType(name="Participation"),
            AssignmentType(name="Presentation"),
            AssignmentType(name="Project"),
            AssignmentType(name="Paper"),
            AssignmentType(name="Test"),
            AssignmentType(name="Quiz"),
        ])

        # Departments/Measurement Topics/Benchmarks out of the Benchmark model
        self.dept1 = Department.objects.create(name="Mathematics")
        self.dept2 = Department.objects.create(name="Science")
        self.dept3 = Department.objects.create(name="Social Studies")


        self.measurement_topic1 = MeasurementTopic.objects.create(
            name="Problem Solving", department=self.dept1)
        self.measurement_topic2 = MeasurementTopic.objects.create(
            name="Reasoning and Proof", department=self.dept1)
        self.measurement_topic3 = MeasurementTopic.objects.create(
            name="Functions", department=self.dept1)
        self.measurement_topic4 = MeasurementTopic.objects.create(
            name="Geographic Thinking", department=self.dept3)
        self.measurement_topic5 = MeasurementTopic.objects.create(
            name="Historical Analysis", department=self.dept3)
        self.measurement_topic6 = MeasurementTopic.objects.create(
            name="Reading Informational Texts", department=self.dept3)

        
        self.benchmark01 = Benchmark.objects.create(
            number="04.09.1", 
            name="Use mathematical symbols and variables to express a " \
                    "constant or linear relationship between quantities")
        self.benchmark02 = Benchmark.objects.create(
            number="04.09.2", 
            name="Recognize which type of expression best fits the " \
                "context of a basic application (for example: linear " \
                "equations to solve distance/time problems, direct " \
                "proportion problems")
        self.benchmark03 = Benchmark.objects.create(
            number="04.09.3", 
            name="Recognize and apply appropriate formulas")
        self.benchmark04 = Benchmark.objects.create(
            number="04.09.4", 
            name="Solve word problems that utilize linear functions")
        self.benchmark05 = Benchmark.objects.create(
            number="04.10.1", 
            name="Apply definitions, postulates, and theorems about " \
                "congruent segments and segment addition to find " \
                "unknown lengths")
        self.benchmark06 = Benchmark.objects.create(
            number="04.10.2", 
            name="Apply definitions, postulates, and theorems about " \
                "congruent, complementary, and supplementary angles")
        self.benchmark07 = Benchmark.objects.create(
            number="04.10.3", 
            name="Apply definitions, postulates, and theorems about angles " \
                "formed by perpendicular lines and when parallel lines are " \
                "cut by a transversal to find unknown angle measures")
        self.benchmark08 = Benchmark.objects.create(
            number="04.10.4", 
            name="Solve simple triangle problems using the triangle angle " \
                "sum property and/or the Pythagorean theorem")
        self.benchmark09 = Benchmark.objects.create(
            number="04.10.5", 
            name="Apply right triangle trig to real-life application")
        self.benchmark10 = Benchmark.objects.create(
            number="04.10.6", 
            name="Find and use measures of lateral areas, surface areas, " \
                "and volumes of prisms, pyramids, spheres, cylinders, " \
                "and cones")

        self.benchmark01.measurement_topics.add(self.measurement_topic1)
        self.benchmark02.measurement_topics.add(self.measurement_topic1)
        self.benchmark03.measurement_topics.add(self.measurement_topic1)
        self.benchmark04.measurement_topics.add(self.measurement_topic1)
        self.benchmark05.measurement_topics.add(self.measurement_topic1)
        self.benchmark06.measurement_topics.add(self.measurement_topic1)
        self.benchmark07.measurement_topics.add(self.measurement_topic1)
        self.benchmark08.measurement_topics.add(self.measurement_topic1)
        self.benchmark09.measurement_topics.add(self.measurement_topic1)
        self.benchmark10.measurement_topics.add(self.measurement_topic1)


    def create_100_courses(self):
        self.create_x_courses(courses=100)

    def create_x_courses(self, courses=30, marking_periods=None):
        for i in xrange(courses):
            self.create_course(marking_periods=marking_periods)

    def create_course(self, credits=1, marking_periods=None):
        random_string = ''.join(
            random.choice(
                string.ascii_uppercase + string.digits
            ) for _ in range(6))
        course = Course.objects.create(
            fullname=random_string,
            shortname=random_string,
            credits=credits,
            graded=True)
        section = CourseSection.objects.create(
            name=course.shortname, course_id=course.id)
        for marking_period in marking_periods:
            section.marking_period.add(marking_period)
        return section

    def create_x_student_grades(self, students=30, courses_per=1):
        mps = MarkingPeriod.objects.all()
        self.create_x_courses(marking_periods=mps, courses=courses_per)
        for i in xrange(students):
            random_string = ''.join(
                random.choice(
                    string.ascii_uppercase + string.digits
                ) for _ in range(6))
            student = Student.objects.create(
                first_name=random_string[:5],
                last_name=random_string[:-5],
                username=random_string)
            for course_section in CourseSection.objects.all():
                enrollment = CourseEnrollment.objects.create(
                    course_section=course_section,
                    user=student,
                )
                for mp in mps:
                    grade = Grade(enrollment=enrollment, marking_period=mp)
                    grade.set_grade(random.randint(0, 100))
                    grade.save()

    def create_aa_superuser(self):
        aa = Faculty.objects.create(username="aa", first_name="aa", is_superuser=True, is_staff=True)
        aa.set_password('aa')
        aa.save()

    def create_admissions_choice_data(self):
        LanguageChoice.objects.create( name = "English" )
        EthnicityChoice.objects.create( name = "Hispanic/Latino" )
        HeardAboutUsOption.objects.create( name = "Radio" )
        ReligionChoice.objects.create( name = "Roman Catholic" )
        FeederSchool.objects.create( name = "Adamson Middle" )

    def create_balt_like_sample_data(self):
        self.create_required()
        self.create_course_types()
        self.create_courses()
        self.create_years_and_marking_periods()
        self.assign_marking_periods_to_course_sections()
        self.create_sample_students()

    def create_course_types(self):
        CourseType.objects.create(name='NonCore', weight=0)
        self.non_core = CourseType.objects.get(name='NonCore')
        CourseType.objects.create(name='AP', weight=1, boost=1.0)
        self.ap = CourseType.objects.get(name='AP')
        CourseType.objects.create(name="Honors", weight=1, boost=0.5)
        self.honors = CourseType.objects.get(name="Honors")

    def create_courses(self):
        self.course1 = Course.objects.create(fullname="English", shortname="English", credits=1, course_type=self.ap, graded=True)
        self.course2 = Course.objects.create(fullname="Precalculus", shortname="Precalc", credits=1, graded=True)
        self.course3 = Course.objects.create(fullname="Physics", shortname="Phys", credits=1, graded=True)
        self.course4 = Course.objects.create(fullname="Modern World History", shortname="Hist", credits=1, graded=True)
        self.course5 = Course.objects.create(fullname="Spanish III", shortname="Span", credits=1, graded=True)
        self.course6 = Course.objects.create(fullname="Photojournalism", shortname="Photo", credits=1, course_type=self.non_core, graded=True)
        self.course7 = Course.objects.create(fullname="Faith & Justice", shortname="Faith", credits=1, graded=True)
        self.course8 = Course.objects.create(fullname="Writing Lab 12", shortname="Wrt Lab", credits=1, course_type=self.non_core, graded=True)
        self.course9 = Course.objects.create(fullname="English Honors", shortname="English-H", credits=1, course_type=self.honors, graded=True)
        self.course10 = Course.objects.create(fullname="Precalculus Honors", shortname="Precalc-H", credits=1, course_type=self.honors, graded=True)
        self.course11 = Course.objects.create(fullname="AP Modern World History", shortname="Hist-AP", credits=1, course_type=self.ap, graded=True)
        self.course12 = Course.objects.create(fullname="Spanish III AP", shortname="Span-AP", credits=1, graded=True, course_type=self.ap)
        self.course13 = Course.objects.create(fullname="Faith & Justice Honors", shortname="Faith-H", credits=1, graded=True, course_type=self.honors)

    def create_years_and_marking_periods(self):
        self.year = year = SchoolYear.objects.create(name="balt year", start_date=datetime.date(2014,7,1), end_date=datetime.date(2050,5,1), active_year=True)
        self.mp1 = MarkingPeriod.objects.create(name="1st", weight=0.4, start_date=datetime.date(2014,7,1), end_date=datetime.date(2014,9,1), school_year=year)
        self.mp2 = MarkingPeriod.objects.create(name="2nd", weight=0.4, start_date=datetime.date(2014,7,2), end_date=datetime.date(2014,9,2), school_year=year)
        self.mps1x = MarkingPeriod.objects.create(name="S1X", weight=0.2, start_date=datetime.date(2014,7,2), end_date=datetime.date(2014,9,2), school_year=year)
        self.mp3 = MarkingPeriod.objects.create(name="3rd", weight=0.4, start_date=datetime.date(2014,7,3), end_date=datetime.date(2014,9,3), school_year=year)
        self.mp4 = MarkingPeriod.objects.create(name="4th", weight=0.4, start_date=datetime.date(2014,7,4), end_date=datetime.date(2014,9,4), school_year=year)
        self.mps2x = MarkingPeriod.objects.create(name="S2X", weight=0.2, start_date=datetime.date(2014,7,4), end_date=datetime.date(2014,9,4), school_year=year)

    def assign_marking_periods_to_course_sections(self):
        courses = Course.objects.all()
        self.student = Student.objects.create(
            first_name="Joe", last_name="Student", username="jstudent")
        student = self.student
        mp1 = self.mp1
        mp2 = self.mp2
        mps1x = self.mps1x
        mp3 = self.mp3
        mp4 = self.mp4
        mps2x = self.mps2x
        i = 0
        for course in courses:
            i += 1
            section = CourseSection.objects.create(
                name=course.shortname, course=course)
            setattr(self, 'course_section' + str(i), section)
            section.marking_period.add(self.mp1)
            section.marking_period.add(self.mp2)
            if course.credits > 0:
                section.marking_period.add(self.mps1x)
            section.marking_period.add(self.mp3)
            section.marking_period.add(self.mp4)
            if course.credits > 0:
                section.marking_period.add(self.mps2x)

            if course.shortname in ['English','Precalc','Phys','Hist','Span','Photo','Faith', 'Wrt Lab']:
                # only enroll self.student in these particular classes,
                # the other ones will be used for other students later on
                CourseEnrollment.objects.create(user=student, course_section=section)
        grade_data = [
            [1, mp1, 72.7],
            [1, mp2, 77.5],
            [1, mps1x, 90],
            [1, mp3, 66.5],
            [1, mp4, 73.9],
            [1, mps2x, 79],
            [2,mp1,55],
            [2,mp2,81.4],
            [2, mps1x, 68],
            [2,mp3,73.9],
            [2,mp4,77.2],
            [2, mps2x, 52],
            [3,mp1,69.1],
            [3,mp2,70.4],
            [3, mps1x, 61],
            [3,mp3,73.8],
            [3,mp4,72.3],
            [3, mps2x, 57],
            [4,mp1,92.4],
            [4,mp2,84.4],
            [4, mps1x, 84],
            [4,mp3,72.6],
            [4,mp4,89.1],
            [4, mps2x, 81],
            [5,mp1,80.4],
            [5,mp2,72.1],
            [5, mps1x, 63],
            [5,mp3,74.4],
            [5,mp4,85.8],
            [5, mps2x, 80],
            [6,mp1,92.8],
            [6,mp2,93.6],
            [6,mp3,83.3],
            [6,mp4,90],
            [7,mp1,79.5],
            [7,mp2,83.1],
            [7, mps1x, 70],
            [7,mp3,78.3],
            [7,mp4,88.5],
            [7, mps2x, 82 ],
            [8,mp1,100],
            [8,mp2,100],
            [8,mp3,100],
            [8,mp4,100],
        ]
        final_grade = FinalGrade(grade=70)
        final_grade.set_enrollment(student, self.course_section3)
        final_grade.save()
        for x in grade_data:
            enrollment = CourseEnrollment.objects.get(
                user=student,
                course_section=getattr(self, 'course_section' + str(x[0])))
            grade = Grade.objects.get_or_create(
                enrollment=enrollment, marking_period=x[1])[0]
            grade.grade = x[2]
            grade.save()
        self.grade = Grade.objects.all().first()
        scale = self.scale = GradeScale.objects.create(name="Balt Test Scale")
        GradeScaleRule.objects.create(min_grade=0, max_grade=69.49, letter_grade='F', numeric_scale=0, grade_scale=scale)
        GradeScaleRule.objects.create(min_grade=69.50, max_grade=72.49, letter_grade='D', numeric_scale=1, grade_scale=scale)
        GradeScaleRule.objects.create(min_grade=72.50, max_grade=76.49, letter_grade='C', numeric_scale=2, grade_scale=scale)
        GradeScaleRule.objects.create(min_grade=76.50, max_grade=79.49, letter_grade='C+', numeric_scale=2.5, grade_scale=scale)
        GradeScaleRule.objects.create(min_grade=79.50, max_grade=82.49, letter_grade='B-', numeric_scale=2.7, grade_scale=scale)
        GradeScaleRule.objects.create(min_grade=82.50, max_grade=86.49, letter_grade='B', numeric_scale=3, grade_scale=scale)
        GradeScaleRule.objects.create(min_grade=86.50, max_grade=89.49, letter_grade='B+', numeric_scale=3.5, grade_scale=scale)
        GradeScaleRule.objects.create(min_grade=89.50, max_grade=92.49, letter_grade='A-', numeric_scale=3.7, grade_scale=scale)
        GradeScaleRule.objects.create(min_grade=92.50, max_grade=100, letter_grade='A', numeric_scale=4, grade_scale=scale)
        self.year.grade_scale = scale
        self.year.save()

    def create_sample_students(self):
        self.create_sample_normal_student()
        self.create_sample_honors_student()
        self.create_sample_honors_student_two()

    def create_sample_normal_student(self):
        self.student = Student.objects.create(first_name="Anon", last_name="Student", username="someone")
        shortname_list = ['English','Precalc','Phys','Hist','Span','Photo','Faith', 'Wrt Lab']
        self.enroll_student_in_sections(self.student, shortname_list)

        known_grades = [
            {'section': 'English',   'grades': [72.7, 77.5, 90,   66.5, 73.9, 79  ]},
            {'section': 'Precalc',   'grades': [55,   81.4, 68,   73.9, 77.2, 52 ]},
            {'section': 'Phys',      'grades': [69.1, 70.4, 61,   73.8, 72.3, 57 ]},
            {'section': 'Hist',      'grades': [92.4, 84.4, 84,   72.6, 89.1, 81 ]},
            {'section': 'Span',      'grades': [80.4, 72.1, 63,   74.4, 85.8, 80  ]},
            {'section': 'Photo',     'grades': [92.8, 93.6, None, 83.3, 90,   None ]},
            {'section': 'Faith',     'grades': [79.5, 83.1, 70,   78.3, 88.5, 82 ]},
            {'section': 'Wrt Lab',   'grades': [100,  100,  None, 100,  100,  None ]},
        ]

        self.populate_student_grades(self.student, known_grades)

        # There is an override grade for this student, so let's register that here
        final = FinalGrade(grade=70)
        final.set_enrollment(self.student, self.course_section3)
        final.save()

    def create_sample_honors_student(self):
        # here we have an honors student
        self.honors_student = Student.objects.create(first_name="Snotty", last_name="McGillicuddy", username="snottymc")

        # let's enroll him in each one of these sections
        shortname_list = ['English-H', 'Precalc-H', 'Phys', 'Hist-AP', 'Span', 'Photo', 'Faith', 'Wrt Lab']
        self.enroll_student_in_sections(self.honors_student, shortname_list)

        # now assign these grades to our honors student
        # Format: {'section': name, 'grades': [1, 2, s1x, 3, 4, s2x]
        known_grades = [
            {'section': 'English-H',    'grades': [89.1, 90.1, 89,   83.4, 82.4, 84  ]},
            {'section': 'Precalc-H',    'grades': [95.9, 80.3, 80,   89.5, 77.8, 73  ]},
            {'section': 'Phys',         'grades': [93.2, 89.9, 92,   92.8, 90.4, None ]},
            {'section': 'Hist-AP',      'grades': [87.3, 78.7, 80,   81.1, 85,   None ]},
            {'section': 'Span',         'grades': [91.4, 88.6, 91,   88.1, 88,   71  ]},
            {'section': 'Photo',        'grades': [100,  95,   None, 97.8, 100,  None ]},
            {'section': 'Faith',        'grades': [88.1, 87.3, 88,   88.8, 91.5, None ]},
            {'section': 'Wrt Lab',      'grades': [100,  100,  None, 100,  100,  None ]},
        ]
        self.populate_student_grades(self.honors_student, known_grades)


    def create_sample_honors_student_two(self):
        self.sample_student1 = Student.objects.create(first_name="Price", last_name="Isright", username="priceisright")

        # let's enroll him in each one of these sections
        shortname_list = ['English', 'Precalc', 'Phys', 'Hist', 'Span-AP', 'Photo', 'Faith-H', 'Wrt Lab']
        self.enroll_student_in_sections(self.sample_student1, shortname_list)

        # now assign these grades to our honors student
        # Format: {'section': name, 'grades': [1, 2, s1x, 3, 4, s2x]
        known_grades = [
            {'section': 'English',  'grades': [95, 96, 89,   78, 87, 88  ]},
            {'section': 'Precalc',  'grades': [87, 78, 80,   89, 98, 88  ]},
            {'section': 'Phys',     'grades': [76, 88, 92,   88, 87, 94 ]},
            {'section': 'Hist',     'grades': [79, 90, 80,   76, 99, 90 ]},
            {'section': 'Span-AP',  'grades': [98, 87, 91,   98, 92, 67 ]},
            {'section': 'Photo',    'grades': [88,  98,  67, 84, 92,  90 ]},
            {'section': 'Faith-H',  'grades': [78, 88, 88,   98, 92, 90 ]},
            {'section': 'Wrt Lab',  'grades': [100,  100,  100, 100,  100, 100]},
        ]

        self.populate_student_grades(self.sample_student1, known_grades)

    def enroll_student_in_sections(self, student, shortname_list):
        """
        enroll the student in each section listed in the shortname_list
        """
        for shortname in shortname_list:
            section = CourseSection.objects.get(name=shortname)
            CourseEnrollment.objects.create(user=student, course_section=section)

    def populate_student_grades(self, student, grade_hash):
        """
        helper method for populating a bunch of student grades

        see examples above for syntax of the grade_hash
        """
        marking_periods = [self.mp1, self.mp2, self.mps1x, self.mp3, self.mp4, self.mps2x]
        for grd in grade_hash:
            section = CourseSection.objects.get(name=grd['section'])
            for i in range(6):
                enrollment = CourseEnrollment.objects.get(
                    user=student,
                    course_section=section)
                grade = Grade.objects.get_or_create(
                    enrollment=enrollment,
                    marking_period=marking_periods[i])[0]
                grade.grade = grd['grades'][i]
                grade.save()

