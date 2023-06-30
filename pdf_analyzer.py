import PyPDF2
import re
import os

def count_words_letters(text):
    words = re.findall(r'\b\w+\b', text)
    letters = sum(len(word) for word in words)
    return len(words), letters

def estimate_reading_time(num_words):
    words_per_minute = 200  # Assuming an average reading speed of 200 words per minute
    minutes = num_words / words_per_minute
    return minutes

def pdf_analysis(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        full_text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            full_text += page.extract_text()

        num_words, num_letters = count_words_letters(full_text)
        reading_time_minutes = estimate_reading_time(num_words)

    return num_words, num_letters, num_pages, reading_time_minutes

def get_user_choice(num_files):
    while True:
        choice = input("Enter the number of the PDF file you want to analyze (1-{}): ".format(num_files))
        if not choice.isdigit():
            print("Invalid input. Please enter a number.")
            continue

        choice = int(choice)
        if choice < 1 or choice > num_files:
            print("Invalid input. Please enter a number between 1 and {}.".format(num_files))
            continue

        return choice

if __name__ == "__main__":
    pdfs_folder = "PDFS"
    pdf_files = [file for file in os.listdir(pdfs_folder) if file.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in the 'PDFS' folder.")
    else:
        print("Available PDF files:")
        for i, pdf_file in enumerate(pdf_files, start=1):
            print("{}. {}".format(i, pdf_file))

        choice = get_user_choice(len(pdf_files))
        selected_file = os.path.join(pdfs_folder, pdf_files[choice - 1])

        words, letters, pages, reading_time = pdf_analysis(selected_file)

        print(f"\nAnalysis for {pdf_files[choice - 1]}:")
        print(f"Number of words: {words}")
        print(f"Number of letters: {letters}")
        print(f"Number of pages: {pages}")
        print(f"Estimated reading time: {reading_time:.2f} minutes")
