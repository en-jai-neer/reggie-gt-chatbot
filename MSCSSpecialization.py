def get_class_requirements(major: str, specialization: str) -> str:
    # Convert inputs to lowercase for comparison
    major = major.lower()
    specialization = specialization.lower()

    # Check if the major is valid
    valid_majors = {"cs", "computer science", "comp sci"}
    if major not in valid_majors:
        return f"No class requirements found for major {major}"

    # Define specializations and their requirements
    specializations = {
        "computational perception and robotics": """
        Pick one (1) of:
        CS 6505 Computability, Algorithms, and Complexity
        CS 6515 Introduction to Graduate Algorithms
        CS 6520 Computational Complexity Theory
        CS 6550 Design and Analysis of Algorithms
        CS 7520 Approximation Algorithms
        CS 7530 Randomized Algorithms
        CSE 6140 Computational Science and Engineering Algorithms
        And pick one of:
        CS 6601 Artificial Intelligence
        CS 7641 Machine Learning
        And pick three (3) courses from Perception and Robotics, with at least one course from each.
        Perception Classes:
        CS 6475 Computational Photography
        CS 6476 Computer Vision
        CS 7499 3D Reconstruction
        CS 7636 Computational Perception
        CS 7639 Cyber Physical Design and Analysis
        CS 7644 Machine Learning for Robotics
        CS 7650 Natural Language
        Robotics Classes:
        CS 7630 Autonomous Robotics
        CS 7631 Autonomous Multi-Robot Systems
        CS 7633 Human-Robot Interaction
        CS 7638 Artificial Intelligence Techniques for Robotics
        CS 7648 Interactive Robot Learning
        CS 7649 Robot Intelligence: Planning
        """,
        "computer graphics": """
        Pick one (1) of:
        CS 6491 Foundations of Computer Graphics
        CS 6457 Video Game Design
        CS 7496 Computer Animation
        And pick one (1) of:
        CS 6505 Computability, Algorithms, and Complexity
        CS 6515 Introduction to Graduate Algorithms
        Electives (9 hours)
        And pick three (3) from:
        CS 6457 Video Game Design and Programming
        CS 6475 Computational Photography
        CS 6476 Computer Vision
        CS 6491 Foundations of Computer Graphics
        CS 6492 Shape Grammars
        CS 6730 Data Visualization Principles
        CS 7450 Information Visualization
        CS 7496 Computer Animation
        """,
        "computing systems": """
        Pick one (1) of:
        CS 6505 Computability, Algorithms, and Complexity
        CS 6515 Introduction to Graduate Algorithms
        And pick two (2) of:
        CS 6210 Advanced Operating Systems
        CS 6241 Compiler Design
        CS 6250 Computer Networks
        CS 6290 High-Performance Computer Architecture
        CS 6300 Software Development Process OR CS 6301 Advanced Topics in Software Engineering
        CS 6390 Programming Languages
        CS 6400 Database Systems Concepts and Designs
        Any Core Courses in excess of the 9 hour requirement may be used as Computing Systems Electives
        And pick three (3) courses from:
        CS 6035 Introduction to Information Security
        CS 6200 Graduate Introduction to Operating Systems
        CS 6220 Big Data Systems and Analytics
        CS 6235 Real Time Systems
        CS 6238 Secure Computer Systems
        CS 6260 Applied Cryptography
        CS 6262 Network Security
        CS 6263 Intro to Cyber Physical Systems Security
        CS 6291 Embedded Software Optimization
        CS 6310 Software Architecture and Design
        CS 6340 Software Analysis and Testing
        CS 6365 Introduction to Enterprise Computing
        CS 6422 Database System Implementation
        CS 6550 Design and Analysis of Algorithms
        CS 6675 Advanced Internet Computing Systems and Applications
        CS 7210 Distributed Computing
        CS 7260 Internetworking Architectures and Protocols
        CS 7270 Networked Applications and Services
        CS 7280 Network Science
        CS 7290 Advanced Topics in Microarchitecture
        CS 7292 Reliability and Security in Computer Architecture
        CS 7560 Theory of Cryptography
        CS 8803 FPL Special Topics: Foundations of Programming Languages
        CSE 6220 High Performance Computing
        """,
        "high performance computing": """
        Must Take:
        CSE 6140 Computational Science and Engineering Algorithms
        CSE 6220 High Performance Computing

        And pick three (3) from:
        CSE 6221 Multicore Computing: Concurrency and Parallelism on the Desktop
        CS/CSE 6230 High-Performance Parallel Computing: Tools and Applications
        CS 6241 Compiler Design
        CS 6290 High-Performance Computer Architecture
        CS/CSE 8803 Special Topics: Parallel Numerical Algorithms
        CSE 6236 Parallel and Distributed Simulation
        CSE 8803 Special Topics: Hot Topics in Parallel Computing
        """,
        "Human Centered Computing": """
        Must Take:
        CS 6451 Intro to HCC
        CS 6452 Prototyping Interactive Systems
        CS 7455 Issues in HCC

        And pick two (2) from:
        CS 6455 User Interface Design and Evaluation
        CS 6456 User Interface Software
        CS 6460 Educational Technology: Conceptual Foundations
        CS 6465 Computational Journalism
        CS 6470 Design of Online Communities
        CS 6471 Computational Social Science
        CS 6474 Social Computing
        CS 6476 Computer Vision
        CS 6601 Artificial Intelligence
        CS 6730 Data Visualization: Principles & Applications
        CS 6750 Human-Computer Interaction
        CS 6795 Introduction to Cognitive Science
        CS 7450 Information Visualization
        CS 7451 Human-Centered Data Analysis
        CS 7460 Collaborative Computing
        CS 7470 Mobile and Ubiquitous Computing
        CS 7476 Advanced Computer Vision
        CS 7610 Modeling and Design
        CS 7632 Game AI
        CS 7633 Human Robot Interaction
        CS 7637 Knowledge-Based AI
        CS 7620 Case-based Reasoning
        CS 7641 Machine Learning
        CS 7650 Natural Language
        CS 7695 Philosophy of Cognition
        CS 7697 Cognitive Models of Science and Technology
        CS 7790 Cognitive Modeling
        CS 8803 Computational Creativity
        CS 8803 Expressive AI
        CS 8803 Computers, Communications & International Development
        """,
        "human-computer interaction": """
        Must Take:
        CS 6456 Principles of User Interface Software OR CS 7470 Mobile and Ubiquitous Computing
        CS 6750 Human-Computer Interaction

        And pick three (3) courses from the two sub-areas below, including at least one from each sub-area:

        Sub-area: Design and evaluation concepts
        CS 6010 Principles of Design
        CS 6320 Software Requirements Analysis and Specification
        CS 6435 Digital Health Equity
        CS 6455 User Interface Design and Evaluation
        CS 6457 Video Game Design
        CS 6460 Educational Technology: Conceptual Foundations
        CS 6465 Computational Journalism
        CS 6470 Design of Online Communities
        CS 6795 Introduction to Cognitive Science
        CS 7465 Educational Technology: Design and Evaluation
        CS 7467 Computer-Supported Collaborative Learning
        CS 7790 Cognitive Modeling

        Sub-area: Interactive technology
        CS 6440 Introduction to Health Informatics
        CS 6730 Data Visualization: Principles & Applications
        CS 6763 Design of Design Environments
        CS 6770 Mixed Reality Experience Design
        CS 7450 Information Visualization
        CS 7451 Human-Centered Data Analysis
        CS 7460 Collaborative Computing
        CS 7470 Mobile and Ubiquitous Computing
        CS 7632 Game AI
        """,
        "interactive intelligence": """
        Take one (1) course from:
        CS 6300 Software Development Process
        CS 6301 Advanced Topics in Software Engineering
        CS 6505 Computability, Algorithms, and Complexity
        CS 6515 Introduction to Graduate Algorithms
        CSE 6140  Computational Science and Engineering Algorithms

        And, two (2) courses from:​
        CS 6601 Artificial Intelligence
        CS 7637 Knowledge-Based AI
        CS 7641 Machine Learning

        And pick two (2) courses from:
        CS 6440 Introduction to Health Informatics
        CS 6460 Educational Technology: Conceptual Foundations
        CS 6465 Computational Journalism
        CS 6471 Computational Social Science
        CS 6603 AI, Ethics, and Society
        CS 6750 Human-Computer Interaction 
        CS 6476 Computer Vision
        CS 7631 Multi-Robot Systems
        CS 7632 Game AI
        CS 7633 Human-Robot Interaction
        CS 7634 AI Storytelling in Virtual Worlds
        CS 7643 Deep Learning
        CS 7647 Machine Learning with Limited Supervision
        CS 7650 Natural Language
        CS 8803 Special Topics: Advanced Game AI
        CS 6795 Introduction to Cognitive Science
        CS 7610 Modeling and Design
        CS 7651 Human and Machine Learning
        CS 8803 Special Topics: Computational Creativity
        """,
        "machine learning": """
        Pick one (1) of:
        CS 6505 Computability, Algorithms, and Complexity
        CS 6515 Introduction to Graduate Algorithms
        CS 6520 Computational Complexity Theory
        CS 6550 Design and Analysis of Algorithms
        CS 7510 Graph Algorithms
        CS 7520 Approximation Algorithms
        CS 7530 Randomized Algorithms
        CSE 6140 Computational Science and Engineering Algorithms

        And, pick one (1) of:
        CS 7641 Machine Learning
        CSE 6740 Computational Data Analysis: Learning, Mining, and Computation

        And pick three (3) of:
        CS 6220 Big Data Systems & Analysis
        CS 6476 Computer Vision 
        CS 6603 AI, Ethics, and Society
        CS 7280 Network Science
        CS 7535 Markov Chain Monte Carlo
        CS 7540 Spectral Algorithms
        CS 7545 Machine Learning Theory
        CS 7616 Pattern Recognition
        CS 7626 Behavioral Imaging 
        CS 7642 Reinforcement Learning and Decision Making
        CS 7643 Deep Learning 
        CS 7644 Machine Learning for Robotics
        CS 7646 Machine Learning for Trading
        CS 7650 Natural Language
        CS 8803 Special Topics: Probabilistic Graph Models
        CSE 6240 Web Search and Text Mining
        CSE 6242 Data and Visual Analytics
        CSE 6250 Big Data for Health
        ISYE 6416 Computational Statistics
        ISYE 6420 Bayesian Methods
        ISYE 6664 Stochastic Optimization
        Approved Substitutions: https://www.cc.gatech.edu/approved-substitutions-specialization-machine-learning-electives
        """,
        "modeling and simulations": """
        Must Take:
        CSE 6730 Modeling and Simulation: Foundations and Implementation

        And pick one (1) of
        CSE 6220 High Performance Computing
        ISYE 6644 Simulation
        MATH 6640 Introduction to Numerical Methods for Partial Differential Equations

        And pick three (3) of:
        CSE 6220 High Performance Computing 
        CSE 6236 Parallel and Distributed Simulation
        CSE/CHEM 8803 Special Topics: Quantum Information, Computation, and Simulation
        CS 7280 Network Science
        INTA 6742 Modeling, Simulation and Military Gaming
        ISYE 6644 Simulation
        MATH 6640 Introduction to Numerical Methods for Partial Differential Equations
        """,
        "scientific computing": """
        Must Take:
        CSE/MATH 6643 Numerical Linear Algebra

        And pick one (1) of:
        CSE/MATH 6644 Iterative Methods for Systems of Equations
        MATH 6640 Introduction to Numerical Methods for Partial Differential Equations

        And pick three (3) of:
        CS/CSE 6230 High-Performance Parallel Computing: Tools and Applications
        CS/CSE 8803 Special Topics: Parallel Numerical Algorithms
        CSE 6140 Computational Science and Engineering Algorithms
        CSE 6220 High Performance Computing
        CSE/MATH 6644 Iterative Methods for Systems of Equations
        CSE 8803 Special Topics: Algorithms for Medical Imaging and Inverse Problems
        CSE 8803/CHEM 6485 Computational Chemistry
        MATH 6640 Introduction to Numerical Methods for Partial Differential Equations
        """,
        "social computing": """
        Pick two (2) of:
        CS 6470 Design of Online Communities
        CS 6474 Social Computing
        CS 6471 Computational Social Science

        And pick three (3) more classes including additional classes from the above and:
        CS 6238 Secure Computer Systems
        CS 6250 Computer Networks
        CS 6456 Principles of User Interface Software
        CS 6465 Computational Journalism
        CS 6505 Computability, Algorithms, and Complexity
        CS 6515 Introduction to Graduate Algorithms 
        CS 6675 Advanced Internet Computing Systems and Applications
        CS 6730 Data Visualization: Principles & Applications
        CS 6750 Human-Computer Interaction
        CS 7210 Distributed Computing
        CS 7270 Networked Applications and Services
        CS 7280 Network Science
        CS 7450 Information Visualization
        CS 7451 Human-Centered Data Analysis
        CS 7467 Computer-Supported Collaborative Learning
        CS 7650 Natural Language

        Specialization: Visual Analytics
        Must Take:
        CS 6730 Data Visualization: Principles & Applications
        CS 7450 Information Visualization
        CSE 6242 Data and Visual Analytics

        And pick two (2) from:
        CS 6456 Principles of User Interface Software
        CS 6465 Computational Journalism
        CS 6491 Computer Graphics
        CS 6750 Human-Computer Interaction
        CS 6795 Introduction to Cognitive Science
        CS 7451 Human-Centered Data Analysis
        CS 7641 Machine Learning
        CSE 6740 Computational Data Analysis
        """
    }

    # Define mappings for shortened specialization names
    specialization_aliases = {
        "computational perception and robotics": {"computational perception and robotics", "cpr"},
        "computer graphics": {"computer graphics", "cg"},
        "computing systems": {"computing systems", "csys", "comp sys"},
        "high performance computing": {"high performance computing", "hpc"},
        "human centered computing": {"human centered computing", "hcc"},
        "human-computer interaction": {"human-computer interaction", "hci"},
        "interactive intelligence": {"interactive intelligence", "ii"},
        "machine learning": {"machine learning", "ml"},
        "modeling and simulations": {"modeling and simulations", "ms"},
        "scientific computing": {"scientific computing", "sc", "scico"},
        "social computing": {"social computing", "soc", "soco"}
    }

    # Find the matching specialization
    for spec_name, aliases in specialization_aliases.items():
        if specialization in aliases:
            return specializations[spec_name]

    return "Specialization not found in available MSCS Specializations"


if __name__ == '__main__':
    major = "Computer Science"
    specialization = "ml"
    requirements = get_class_requirements(major, specialization)
    print(requirements)
    print()