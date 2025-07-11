# 📝 Worksheet Generator for Teachers

A clean, powerful Streamlit app that helps primary school teachers automatically generate daily arithmetic worksheets for students — without writing the same questions over and over again!

---

## 🎯 What It Does

This app allows you to:
- Generate **addition, subtraction, multiplication, and division** questions
- Choose between two worksheet modes:
  - **UNIQUE**: Each student gets a different set of questions
  - **SAME**: All students get the same worksheet
- Customize:
  - Number of students
  - Number of questions per operation
  - Digit-length of operands (1 to 6 digits)
- Add custom instructions at the top of the worksheet
- Export a clean, printable **PDF** for each student or a shared one for all

---

## 🛠️ Tech Stack

- **Python 3.10**
- **Streamlit** – UI framework
- **NumPy** – Random number generation
- **FPDF** – PDF generation
- **Pillow (optional)** – For adding visual elements if needed

---

## 🚀 Getting Started

### 1. Clone this repository

```bash
git clone https://github.com/yourusername/worksheet-generator.git
cd worksheet-generator
