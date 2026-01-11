from rest_framework_csv.renderers import CSVRenderer
import csv
import io
from .models import Expense
from categories.models import Category
from expense_tracker.utils import parse_date

def process_expense_csv(file_obj, user):
    """
    Parses a CSV file and creates Expense records.
    Returns a dict with summary (count, errors).
    """
    # 1. Read the file content from memory
    decoded_file = file_obj.read().decode('utf-8')
    
    # 2. Convert string to a file-like object so CSV reader can process it
    io_string = io.StringIO(decoded_file)
    
    # 3. Initialize the CSV Dictionary Reader (Keys = Header Row)
    reader = csv.DictReader(io_string)

    # 4. Initialize counters and error list
    imported_count = 0
    errors = []
    
    # 5. Pre-fetch 'Expense' type categories to avoid Database hits in the loop
    # We store them as {'food': <CategoryObj>, 'travel': <CategoryObj>} for easy lookup
    # Dictionary Comprehension feature.
    valid_categories = {
        category.name.lower(): category 
        for category in Category.objects.filter(type='expense', owner=user)
    }

    # 6. Iterate through each row in the CSV
    # We use enumerate(reader, start=2) because row 1 is header
    for row_number, row_data in enumerate(reader, start=2):
        
        # 7. Clean the keys (headers) just in case (e.g. ' Title ' -> 'title')
        # We also lower-case them to be case-insensitive
        clean_row = {
            key.lower().strip(): value 
            for key, value in row_data.items() 
            if key # Ignore empty keys (trailing commas)
        }
        
        # 8. Extract the Category Name from the row
        input_category_name = clean_row.get('category', '').strip()
        
        # 9. Look for this category in our pre-fetched list (Case Insensitive)
        category_obj = valid_categories.get(input_category_name.lower())
        
        # 10. Validation: If category is invalid or missing, record error and Skip
        if not category_obj:
            error_msg = f"Row {row_number}: Category '{input_category_name}' not found or valid."
            errors.append(error_msg)
            continue

        # 11. Create the Expense Record
        try:
            Expense.objects.create(
                owner=user,
                title = clean_row.get('title'),
                amount = clean_row.get('amount'),
                category = category_obj, # Assignment the Foreign Key Object
                entry_date = parse_date(clean_row.get('date')), # Helper to parse '2026-01-05' etc
                payment_method = clean_row.get('payment_method', 'cash'), # Default to cash
                description = clean_row.get('description', '')
            )
            
            # 12. Increment success counter
            imported_count += 1
            
        except Exception as e:
            # 13. Catch any other errors (like invalid Amount) and record them
            errors.append(f"Row {row_number}: {str(e)}")

    # 14. Return the Final Summary
    return {
        "status": "success",
        "imported_count": imported_count,
        "errors": errors
    }

class ExpenseCSVRenderer(CSVRenderer):
    """
    Custom CSV Renderer to define headers and labels for Expense Export.
    This keeps the View code clean and separates formatting logic.
    """
    # The columns to include in the CSV (must match serializer fields)
    header = [
        'id', 
        'title', 
        'category_name', 
        'category_type', 
        'amount', 
        'entry_date', 
        'payment_method', 
        'description'
    ]

    # Friendly names for the CSV Header Row
    labels = {
        'id': 'ID',
        'title': 'Expense Title',
        'category_name': 'Category',
        'category_type': 'Type',
        'amount': 'Amount (USD)',
        'entry_date': 'Date',
        'payment_method': 'Payment By',
        'description': 'Description'
    }
