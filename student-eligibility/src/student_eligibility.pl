:- use_module(library(http/thread_httpd)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(http/http_parameters)).
:- use_module(library(http/http_json)).
:- use_module(library(http/http_cors)).

% Load student data from CSV
load_student_data :-
    % Retract any existing facts first
    retractall(student(_, _, _)),
    
    % Open and read the file
    open('students.csv', read, Stream),
    read_csv_data(Stream),
    close(Stream).

% Read CSV data line by line
read_csv_data(Stream) :-
    \+ at_end_of_stream(Stream),
    !,
    read_line_to_string(Stream, Line),
    % Split line and convert to student fact
    (   Line \= end_of_file,
        Line \= "",
        split_string(Line, ",", " \t\n", [StudentID, AttendanceStr, CGPAStr]),
        atom_number(AttendanceStr, Attendance),
        atom_number(CGPAStr, CGPA),
        assertz(student(StudentID, Attendance, CGPA))
    ;   true),
    read_csv_data(Stream).
read_csv_data(_).

% Start server
server(Port) :-
    load_student_data,
    http_server(http_dispatch, [port(Port)]).

% Route for checking eligibility
:- http_handler(root(check_eligibility), check_eligibility, [methods([get, options])]).

% Rules for scholarship and exam permissions
eligible_for_scholarship(Student_ID) :-
    student(Student_ID, Attendance, CGPA),
    Attendance >= 75,
    CGPA >= 9.0.

permitted_for_exam(Student_ID) :-
    student(Student_ID, Attendance, _),
    Attendance >= 75.

% Handle eligibility requests
check_eligibility(Request) :-
    cors_enable(Request, [methods([get, options])]), % Enable CORS
    (   memberchk(method(options), Request)  % Handle preflight OPTIONS
    ->  format('~n')
    ;   % Handle GET requests
        http_parameters(Request, [student_id(Student_ID, [string])]),
        % Check eligibility
        (   eligible_for_scholarship(Student_ID)
        ->  Scholarship = true
        ;   Scholarship = false ),
        
        (   permitted_for_exam(Student_ID)
        ->  ExamPermission = true
        ;   ExamPermission = false ),
        
        Reply = json{scholarship: Scholarship, exam_permission: ExamPermission},
        format('Access-Control-Allow-Origin: *~n'),
        reply_json(Reply)
    ).

% Debugging predicate
debug_students :-
    findall(row(ID, Attendance, CGPA), student(ID, Attendance, CGPA), Students),
    print(Students).

% Start server on port 8000
:- initialization(server(8000)).