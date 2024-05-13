from django.shortcuts import render
from django.http import HttpResponse

import pandas as pd

def index(request):
    book_data = None  # Initialize variable to hold book data
    file_selected = False  # Flag to check if file was selected
    column_stats = None  # Variable to hold column statistics
    max_rows = 100  # Maximum number of rows to display

    if request.method == 'POST':
        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']

            # Check if the uploaded file is a CSV file
            if not csv_file.name.endswith('.csv'):
                return HttpResponse('File is not a CSV')

            # Use pandas to read the CSV file
            try:
                df = pd.read_csv(csv_file)
                # Now you have a DataFrame 'df' containing your CSV data
                # You can pass this data to the template for rendering
                book_data = df.head(max_rows).to_dict(orient='records')

                # Calculate mean and median for each numeric column
                column_stats = df.select_dtypes(include='number').agg(['mean', 'median'])

                file_selected = True  # Set flag to True as file was selected and processed

            except pd.errors.ParserError as e:
                return HttpResponse(f'Error parsing CSV file: {e}')

    return render(request, 'index.html', {'book_data': book_data, 'file_selected': file_selected, 'column_stats': column_stats})

def analytics(request):
    return render(request, 'anime_pp/analytics.html')


def clean_data(request):
    # Add your data cleaning logic here
    # For example, you can use pandas to clean the DataFrame
    cleaned_data = df  # Replace 'df' with your cleaned DataFrame
    return HttpResponse('Data cleaned successfully')
