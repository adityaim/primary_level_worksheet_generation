
import streamlit as st
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
import random
import time
import os

# def serve_google_verification():
#     if st.query_params.get("verify") == "google15fc09166f3671ca":
#         with open("google15fc09166f3671ca.html", "r") as file:
#             html = file.read()
#             st.markdown(html, unsafe_allow_html=True)
#         st.stop()

# serve_google_verification()
st.set_page_config(
    page_title="Arithmetic Worksheet Generator",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;600&family=Playfair+Display:wght@400;700&display=swap');
.main-header {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    color: #2c3e50;
    text-align: center;
    margin-bottom: 2rem;
    font-weight: 700;
    letter-spacing: 1px;
}
.sub-header {
    font-family: 'Crimson Text', serif;
    font-size: 1.2rem;
    color: #34495e;
    text-align: center;
    margin-bottom: 3rem;
    font-style: italic;
}
.stApp {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}
.stButton > button {
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
    color: white;
    border: none;
    padding: 0.5rem 2rem;
    font-family: 'Crimson Text', serif;
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    border-radius: 8px;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(44, 62, 80, 0.3);
}
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > div,
.stTextArea > div > div > textarea {
    background: rgba(255, 255, 255, 0.95);
    border: 2px solid #2c3e50;
    border-radius: 8px;
    font-family: 'Crimson Text', serif;
    font-size: 1.1rem;
}
.loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}
.loading-spinner {
    width: 50px;
    height: 50px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
.loading-message {
    font-family: 'Crimson Text', serif;
    font-size: 1.2rem;
    color: #2c3e50;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

if 'step' not in st.session_state:
    st.session_state.step = 'start'
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'operation_info' not in st.session_state:
    st.session_state.operation_info = []
if 'num_students' not in st.session_state:
    st.session_state.num_students = 1
if 'mode' not in st.session_state:
    st.session_state.mode = 'SAME'

def generate_questions(operation, num_questions, digit_specs, mode, num_students):
    questions = []
    if operation == "Addition":
        digits = digit_specs['digits']
        for _ in range(num_questions):
            a = np.random.randint(10**(digits-1), 10**digits)
            b = np.random.randint(10**(digits-1), 10**digits)
            questions.append(f"{a} + {b} = ")
    elif operation == "Subtraction":
        digits_a = digit_specs['digits_a']
        digits_b = digit_specs['digits_b']
        for _ in range(num_questions):
            a = np.random.randint(10**(digits_a-1), 10**digits_a)
            b = np.random.randint(10**(digits_b-1), min(10**digits_b, a))
            questions.append(f"{a} - {b} = ")
    elif operation == "Multiplication":
        digits_a = digit_specs['digits_a']
        digits_b = digit_specs['digits_b']
        for _ in range(num_questions):
            a = np.random.randint(10**(digits_a-1), 10**digits_a)
            if digits_b == 1:
                b = np.random.randint(2, 10)  # Exclude 1
            else:
                b = np.random.randint(10**(digits_b-1), 10**digits_b)
            questions.append(f"{a} × {b} = ")
    elif operation == "Division":
        digits_a = digit_specs['digits_a']
        digits_b = digit_specs['digits_b']
        for _ in range(num_questions):
            if digits_b == 1:
                b = np.random.randint(2, 10)  # Exclude 1
            else:
                b = np.random.randint(10**(digits_b-1), 10**digits_b)
            quotient = np.random.randint(1, 100)
            a = b * quotient
            questions.append(f"{a} ÷ {b} = ")
    
    if mode == "UNIQUE":
        all_questions = []
        for _ in range(num_students):
            student_questions = []
            for _ in range(num_questions):
                if operation == "Addition":
                    a = np.random.randint(10**(digits-1), 10**digits)
                    b = np.random.randint(10**(digits-1), 10**digits)
                    student_questions.append(f"{a} + {b} = ")
                elif operation == "Subtraction":
                    a = np.random.randint(10**(digits_a-1), 10**digits_a)
                    b = np.random.randint(10**(digits_b-1), min(10**digits_b, a))
                    student_questions.append(f"{a} - {b} = ")
                elif operation == "Multiplication":
                    a = np.random.randint(10**(digits_a-1), 10**digits_a)
                    if digits_b == 1:
                        b = np.random.randint(2, 10)
                    else:
                        b = np.random.randint(10**(digits_b-1), 10**digits_b)
                    student_questions.append(f"{a} × {b} = ")
                elif operation == "Division":
                    if digits_b == 1:
                        b = np.random.randint(2, 10)
                    else:
                        b = np.random.randint(10**(digits_b-1), 10**digits_b)
                    quotient = np.random.randint(1, 100)
                    a = b * quotient
                    student_questions.append(f"{a} ÷ {b} = ")
            all_questions.append(student_questions)
        return all_questions
    else:
        return questions

def create_pdf(questions_data, instructions, mode, num_students, operation_info):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    student_info_style = ParagraphStyle(
        'StudentInfo',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=25,
        alignment=TA_LEFT,
        fontName='Helvetica'
    )
    instruction_style = ParagraphStyle(
        'Instructions',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=25,
        alignment=TA_LEFT,
        fontName='Helvetica'
    )
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=15,
        spaceBefore=25,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold'
    )
    question_style = ParagraphStyle(
        'Questions',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=15,
        alignment=TA_LEFT,
        fontName='Helvetica',
        leftIndent=20
    )
    story = []
    for student_idx in range(num_students):
        if student_idx > 0:
            story.append(PageBreak())
        story.append(Paragraph("Mathematics Worksheet", title_style))
        story.append(Paragraph("Name: _____________________________     Date: _______________", student_info_style))
        story.append(Paragraph(f"<b>Instructions:</b> {instructions}", instruction_style))
        student_questions = questions_data[student_idx]
        for section_idx, (operation_questions, operation_name) in enumerate(zip(student_questions, operation_info)):
            story.append(Paragraph(f"Section {section_idx + 1}: {operation_name}", section_style))
            for question_idx, question in enumerate(operation_questions):
                if not isinstance(question, str):
                    question = str(question)
                story.append(Paragraph(f"{question_idx + 1}) {question}", question_style))
            story.append(Spacer(1, 20))
    doc.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data

def show_loading_spinner():
    beautiful_messages = [
        "Weaving mathematical symphonies with threads of wisdom...",
        "Crafting educational masterpieces in the forge of knowledge...",
        "Sculpting numbers into pathways of understanding...",
        "Brewing the perfect blend of challenge and learning...",
        "Transforming digits into doorways of discovery...",
        "Painting problems with the brushstrokes of brilliance...",
        "Orchestrating equations in the concert hall of education...",
        "Cultivating gardens of mathematical growth and wonder..."
    ]
    message = random.choice(beautiful_messages)
    st.markdown(f"""
    <div class="loading-container">
    <div class="loading-spinner"></div>
    <div class="loading-message">{message}</div>
    </div>
    """, unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">Arithmetic Worksheet Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Crafting mathematical excellence, one worksheet at a time</p>', unsafe_allow_html=True)

    if st.session_state.step == 'start':
        st.markdown('<h3 class="step-title">Class Configuration</h3>', unsafe_allow_html=True)
        num_students = st.text_input(
            "How many students will receive worksheets?",
            value="1",
            help="Enter the number of students in your class"
        )
        try:
            num_students = int(num_students)
            if num_students < 1 or num_students > 100:
                st.error("Please enter a number between 1 and 100")
                return
        except ValueError:
            st.error("Please enter a valid number")
            return
        mode = st.selectbox(
            "Choose worksheet distribution mode:",
            ["SAME", "UNIQUE"],
            help="SAME: All students get identical questions | UNIQUE: Each student gets different questions"
        )
        if st.button("Continue to Question Setup"):
            st.session_state.num_students = num_students
            st.session_state.mode = mode
            st.session_state.step = 'operations'
            st.rerun()

    elif st.session_state.step == 'operations':
        st.markdown('<h3 class="step-title">Operation Selection</h3>', unsafe_allow_html=True)
        st.write(f"*Configuration:* {st.session_state.num_students} students, {st.session_state.mode} mode")
        operation = st.selectbox(
            "Select the type of arithmetic operation:",
            ["Addition", "Subtraction", "Multiplication", "Division"]
        )
        num_questions = st.number_input(
            f"How many {operation.lower()} questions?",
            min_value=1,
            max_value=50,
            value=5
        )
        digit_specs = {}
        if operation == "Addition":
            digits = st.selectbox(
                "Number of digits for each number:",
                [1, 2, 3, 4, 5, 6],
                help="Both numbers will have this many digits"
            )
            digit_specs['digits'] = digits
        elif operation in ["Subtraction", "Multiplication", "Division"]:
            col1, col2 = st.columns(2)
            with col1:
                digits_a = st.selectbox(
                    "Digits in first number:",
                    [1, 2, 3, 4, 5, 6],
                    key=f"{operation.lower()}_a"
                )
            with col2:
                digits_b = st.selectbox(
                    "Digits in second number:",
                    [1, 2, 3, 4, 5, 6],
                    key=f"{operation.lower()}_b"
                )
            digit_specs['digits_a'] = digits_a
            digit_specs['digits_b'] = digits_b
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Add These Questions"):
                questions = generate_questions(
                    operation, num_questions, digit_specs,
                    st.session_state.mode, st.session_state.num_students
                )
                st.session_state.questions.append(questions)
                st.session_state.operation_info.append(operation)
                st.success(f"Added {num_questions} {operation.lower()} questions!")
        with col2:
            if st.button("Finish & Add Instructions"):
                if st.session_state.questions:
                    st.session_state.step = 'instructions'
                    st.rerun()
                else:
                    st.error("Please add at least one set of questions first!")
        if st.session_state.operation_info:
            st.markdown("### Current Questions Added:")
            for i, op in enumerate(st.session_state.operation_info, 1):
                num_qs = len(st.session_state.questions[i-1][0]) if st.session_state.mode == "UNIQUE" else len(st.session_state.questions[i-1])
                st.write(f"{i}. {op} ({num_qs} questions)")

    elif st.session_state.step == 'instructions':
        st.markdown('<h3 class="step-title">Worksheet Instructions</h3>', unsafe_allow_html=True)
        st.write(f"*Final Configuration:* {st.session_state.num_students} students, {st.session_state.mode} mode")
        st.write(f"*Questions Added:* {', '.join(st.session_state.operation_info)}")
        st.markdown("---")
        st.markdown("### Add Instructions for Students")
        instructions = st.text_area(
            "Enter instructions for the worksheet:",
            value="Solve the following problems neatly. Show all your work.",
            height=100,
            help="These instructions will appear at the top of every worksheet"
        )
        if st.button("Generate PDF Worksheets"):
            loading_placeholder = st.empty()
            with loading_placeholder.container():
                show_loading_spinner()
                time.sleep(2)  # Simulate processing time
            try:
                if st.session_state.mode == "SAME":
                    pdf_questions = [st.session_state.questions] * st.session_state.num_students
                else:
                    pdf_questions = []
                    for student_idx in range(st.session_state.num_students):
                        student_questions = [questions[student_idx] for questions in st.session_state.questions]
                        pdf_questions.append(student_questions)
                pdf_data = create_pdf(
                    pdf_questions, instructions,
                    st.session_state.mode, st.session_state.num_students,
                    st.session_state.operation_info
                )
                loading_placeholder.empty()
                st.success("Worksheets generated successfully!")
                filename = f"arithmetic_worksheets_{st.session_state.mode.lower()}_{st.session_state.num_students}students.pdf"
                st.download_button(
                    label="Download PDF Worksheets",
                    data=pdf_data,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True
                )
                if st.button("Create New Worksheets"):
                    for key in ['step', 'questions', 'operation_info', 'num_students', 'mode']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
            except Exception as e:
                loading_placeholder.empty()
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()