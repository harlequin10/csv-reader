import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import JsonResponse
from django.conf import settings
import os

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

                # Calculate mean, median, mode, standard deviation, range, max, min, and total rows for each numeric column
                numeric_columns = df.select_dtypes(include='number').columns
                column_stats = {}
                for column in numeric_columns:
                    if 'id' not in column.lower(): # Check if the column is not 'id'
                        column_stats[column] = {
                            'mean': df[column].mean(),
                            'median': df[column].median(),
                            'mode': df[column].mode().values[0],
                            'std': df[column].std(),
                            'min': df[column].min(),
                            'max': df[column].max(),
                            'range': df[column].max() - df[column].min(),
                            'total_rows': len(df)
                        }

                file_selected = True  # Set flag to True as file was selected and processed

            except pd.errors.ParserError as e:
                return HttpResponse(f'Error parsing CSV file: {e}')

    return render(request, 'index.html', {'book_data': book_data, 'file_selected': file_selected, 'column_stats': column_stats})

def analytics(request):
    return render(request, 'anime_pp/analytics.html')


def clean_data(request):
    if request.method == 'POST':
        # Retrieve the uploaded file from the session
        uploaded_file = request.session.get('uploaded_file')

        if not uploaded_file:
            return HttpResponse('No file uploaded')

        # Read the uploaded file into a pandas DataFrame
        try:
            print("Reading CSV file...")
            df = pd.read_csv(uploaded_file)
            print("CSV file read successfully.")

            # Add your data cleaning logic here
            # For example, you can remove rows with missing values
            print("Cleaning data...")
            cleaned_data = df.dropna()
            print("Data cleaned successfully.")

            # Convert the cleaned DataFrame to a CSV file
            cleaned_csv = cleaned_data.to_csv(index=False)

            # Prepare the response to return the cleaned CSV file for download
            response = HttpResponse(cleaned_csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="cleaned_data.csv"'

            return response
        except Exception as e:
            return HttpResponse(f'Error cleaning CSV file: {e}')

    return HttpResponse('No file uploaded')
