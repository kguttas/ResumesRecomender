from RecomendadorCurriculums.AutoScreening.model import Utilities
from RecomendadorCurriculums.AutoScreening.model import AutoScreeningModel


# Parámetros

path_model_word2vec = '../data/model_word2vec.bin'

path_resumes = '../../../data/process_resumes'

top_recommendation = 10

text_offer = """
 Function title: Software Engineer (Full-stack Angular/Java Developer)
Reference: NOC-MA-2022-FGIII/400
Location: Maastricht - Information about living in Maastricht
Nature of the competition: Internal and external competition
Applicable regulations: Conditions of Employment of Contract Staff at EUROCONTROL
Grades: AC 8/10 - Check salary simulations for the basic grade
Generic post: Assistant (FG-III) (8/10 )
Number of posts: 2
Duration of engagement: 3 Year (s)
Security clearance: EU/NATO SECRET
Directorate/Service: MAAS/ATM/TS - Technical Systems
Competition publication date: 03/02/2022
Competition closing date: 03/03/2022 (23:59 Brussels time)
Reserve list: Applicable - See details in the "Useful information" section
YOUR TEAM
Within the Directorate Maastricht Upper Area Control Centre , the "Technical Systems" service is responsible for the maintenance, development and improvement of software products which support MUAC in achieving its safety and capacity targets and sustain the growing air traffic demand. It provides also resources to various projects in its area of expertise and maintains technical hardware.

Engineering the future of air traffic control

YOUR ROLE
Your role will be to:

Develop software (Java/Angular2+/TypeScript) in order to maintain and improve the in-house developed automated sectorisation and position assignment tool, and/or the connector between our flight plan server and new client applications:
To analyse technical and operational problem reports, to determine the diagnostics and to fix problems.
To analyse change requests, resulting in lifecycle document changes, safety assessment and test scoping.
To implement changes and bug fixes including demonstration, documentation and unit testing in accordance with the SCRUM methodology.
Support the users of the products that you developed by delivering training, documentation, presentations and advise.
Provide support to other owners of products within the team based on the similar software stack with code reviews and small changes.
Foster the use of DevOps pipelines and software engineering tools such as Jenkins, Nexus, SonarQube.
Participate to projects, work packages, studies whenever required.
Carry out any other task in line with the main purpose of the job.
REQUIRED QUALIFICATIONS, EXPERIENCE & COMPETENCIES
Completed university studies of at least 3 years in a relevant domain (computer science, Engineering, etc) and appropriate professional experience of 1 year.
A minimum of 2 years of relevant working experience of which at least 1 year with Java in the back-end and Angular/TypeScript in the frond-end.
Experience as a full-stack software developer.
Experienced in developing and designing software using Java and Spring Boot in the back-end, and JavaScript/TypeScript, CSS, HTML5 and the Angular framework in the front-end.
The following would be an advantage:
Experience with Jira and Git/Bitbucket.
Experience with the SCRUM methodology.
Experience with ASN-1 and/or XML.
Knowledge of Linux.
Knowledge of Ada, C or C++.
Knowledge of modern service oriented architectures & middleware, message brokers (e.g. ActiveMQ), containers, API integration, data distribution, etc.
Knowledge of DevSecOps pipelines.
Technical writing skills (English).
Communication: Fosters two-way communication.
Analytical Thinking: Analyses information and Identifies relationships.
Teamwork: Fosters teamwork.
Problem Solving: Anticipates and solves business issues.
Quality Focus: Sets and fosters high quality standards.
Ability to work in a multinational and multicultural environment.
Professional conduct in line with the corporate behaviours of the Agency, i.e. result-driven, readiness to change, customer focus, integrity and team-player approach.
The working languages of the Agency are English and French. For this particular job, candidates must be proficient users of English at level C1/C2.
The levels relate to the Common European Framework of References for languages (CEFR).
USEFUL INFORMATION
Applications will be accepted from nationals of EUROCONTROL Member States only.
The selected candidate will be offered a contract of 3 Year (s) pursuant to the provisions of the Conditions of Employment of Contract Staff at EUROCONTROL. The contract may be renewed. Before being established in the post, he/she will be requested to provide certified copies of his/her degrees and successfully serve a probationary period of 9 months.
The successful candidate shall be engaged in principle at the basic grade of the advertised grades.
In case of reserve list: Suitable candidates, however not selected to fill the post, will be placed on a reserve list for similar functions. The period of validity of reserve list is 1 year from the closing date of applications.
Information on salary and benefits can be found on the web page: http://jobs.eurocontrol.int/what-we-offer
EUROCONTROL is committed to non-discrimination and equal opportunities. We welcome applications from all qualified candidates, irrespective of gender, age, disability, race, colour, ethnic or social origin, religion or belief, marital or parental status and sexual orientation.
In the event of equal merit, preference may be given to the applicant from the under-represented diversity characteristics.
Candidates should go to our Jobs website and read the tips on how to apply. Item 1 includes information on the EUROCONTROL competency models (technical & behavioural) – Candidates should refer to the behavioural competency model to know the behaviours expected for the different levels.
 """

############
util = Utilities.Utilities()

df_CVs = util.convert_resumes_files2dataframe(path_resumes)

print(df_CVs.head())

df_offer = util.convert_text_job_offer(text_offer)

print(df_offer)

id_offer = df_offer["_id"].iloc[0]
print(id_offer)

df_for_process = util.concat_joboffer_CVs(df_offer, df_CVs)

#print(df_for_process)

df_text_clean = util.preprocess_text(df_for_process)

#print(df_text_clean)

model = AutoScreeningModel.AutoScreeningModel(path_model_word2vec)

corpus = model.generate_corpus(df_text_clean)

#print(corpus)

model.build_vocab(corpus)

# Solo para probar
most_similar = model.get_most_similar("dharamvirsinghgmailcom")

#print(most_similar)

recommended = model.recommendations(id_offer, df_text_clean, top_recommendation)

print(recommended)

firts_element = recommended[recommended.index == 0]

#print(firts_element["common_texts"].iloc[0])