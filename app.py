# from flask import Flask, render_template, request, send_file
# import boto3
# from botocore.exceptions import NoCredentialsError

# import os
# import re
# import pandas as pd
# from PyPDF2 import PdfReader

# app = Flask(__name__)

# # Configure AWS S3 Client
# s3_client = boto3.client(
#     's3',
#     aws_access_key_id='your-access-key-id',
#     aws_secret_access_key='your-secret-access-key',
#     region_name='your-region'  # Example: 'us-east-1'
# )

# def index():
#     return render_template('index.html')

# # Route for the home page (Upload PDF)
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Route to handle PDF upload and conversion
# @app.route('/upload', methods=['POST'])
# def upload_pdf():
#     # Check if the PDF is part of the request
#     if 'pdf_file' not in request.files:
#         return "No file part", 400
    
#     pdf_file = request.files['pdf_file']

#     if pdf_file.filename == '':
#         return 'No selected file', 400

#     if pdf_file and pdf_file.filename.endswith('.pdf'):
#         try:
#             # Upload the file directly to AWS S3 bucket
#             s3_client.upload_fileobj(pdf_file, 'your-bucket-name', pdf_file.filename)

#             # Generate a public URL for the uploaded file
#             file_url = f'https://{your-bucket-name}.s3.amazonaws.com/{pdf_file.filename}'

#             # Extract data from PDF using the file URL
#             data = extract_data_from_pdf(file_url)

#             # Create DataFrame and add summary
#             df = pd.DataFrame(data)
#             if not df.empty:
#                 total_sum = df["Total"].sum()
#                 total_orders = len(df)
#                 summary_row = {
#                     "Order ID": "TOTAL SUMMARY",
#                     "Order Date": "",
#                     "Deliver To": "",
#                     "Phone": "",
#                     "Delivery Address": "",
#                     "Total": total_sum
#                 }
#                 df = pd.concat([df, pd.DataFrame([summary_row])], ignore_index=True)

#             # Save DataFrame to Excel and return it as a download
#             output_excel = 'Extracted_Order_Details.xlsx'
#             df.to_excel(output_excel, index=False)
#             return send_file(output_excel, as_attachment=True)

#         except NoCredentialsError:
#             return "Credentials not available", 400

#     return "Invalid file format. Please upload a PDF.", 400


# def extract_data_from_pdf(pdf_path):
#     reader = PdfReader(pdf_path)
#     data = []

#     for page in reader.pages:
#         text = page.extract_text()
#         lines = text.split('\n')

#         order_id = ""
#         order_date = ""
#         deliver_to = ""
#         phone = ""
#         delivery_address = ""
#         total = 0.0

#         for idx, line in enumerate(lines):
#             # ---- Parse Order ID ----
#             if "Order ID" in line:
#                 match_id = re.search(r"Order ID\s*(\d+)", line)
#                 if match_id:
#                     order_id = match_id.group(1)
#                 else:
#                     if idx + 1 < len(lines):
#                         next_line_match = re.search(r"(\d+)", lines[idx + 1])
#                         if next_line_match:
#                             order_id = next_line_match.group(1)

#             # ---- Parse Order Date ----
#             if "Order Date" in line:
#                 match_date = re.search(r"Order Date:\s*(.*)", line)
#                 if match_date:
#                     order_date = match_date.group(1).strip()
#                 else:
#                     if idx + 1 < len(lines):
#                         order_date = lines[idx + 1].strip()

#             # ---- Parse Deliver To & Phone ----
#             if "Deliver To:" in line:
#                 dt_match = re.search(r"Deliver To:\s*(.*)", line)
#                 if dt_match:
#                     dt_str = dt_match.group(1).strip()
#                     phone_match = re.search(r"(?i)phone:\s*(\d+)", dt_str)
#                     if phone_match:
#                         phone = phone_match.group(1)
#                         dt_str = re.sub(r"(?i)phone:\s*\d+", "", dt_str).strip()
#                     deliver_to = dt_str

#             # ---- Parse Delivery Address ----
#             if "Delivery Address:" in line:
#                 addr_lines = []
#                 da_match = re.search(r"Delivery Address:\s*(.*)", line)
#                 if da_match:
#                     possible_addr = da_match.group(1).strip()
#                     if possible_addr and not re.search(r'Bill To|Billing Address', possible_addr, re.IGNORECASE):
#                         addr_lines.append(possible_addr)

#                 for j in range(1, 10):
#                     if idx + j < len(lines):
#                         next_line = lines[idx + j].strip()
#                         if "Bill To" in next_line or "Billing Address" in next_line:
#                             break
#                         addr_lines.append(next_line)
#                     else:
#                         break

#                 delivery_address = ', '.join(addr_lines)

#             # ---- Parse Total ----
#             if "Total:" in line:
#                 total_match = re.search(r'Total:\s*([\d,]+\.\d+|\d+)', line)
#                 if total_match:
#                     total = float(total_match.group(1).replace(',', ''))

#         if order_id:
#             data.append({
#                 "Order ID": order_id,
#                 "Order Date": order_date,
#                 "Deliver To": deliver_to,
#                 "Phone": phone,
#                 "Delivery Address": delivery_address,
#                 "Total": total
#             })

#     return data


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')






# from flask import Flask, render_template, request, send_file
# import boto3
# from botocore.exceptions import NoCredentialsError

# import os
# import re
# import pandas as pd
# from PyPDF2 import PdfReader

# app = Flask(__name__)

# # Configure AWS S3 Client
# s3_client = boto3.client(
#     's3',
#     aws_access_key_id='your-access-key-id',
#     aws_secret_access_key='your-secret-access-key',
#     region_name='your-region'  # Example: 'us-east-1'
# )

# def index():
#     return render_template('index.html')

# # Route for the home page (Upload PDF)
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Route to handle PDF upload and conversion
# @app.route('/upload', methods=['POST'])
# def upload_pdf():
#     try:
#         # Check if the PDF is part of the request
#         if 'pdf_file' not in request.files:
#             return "No file part", 400
        
#         pdf_file = request.files['pdf_file']

#         if pdf_file.filename == '':
#             return 'No selected file', 400

#         if pdf_file and pdf_file.filename.endswith('.pdf'):
#             # Upload the file directly to AWS S3 bucket
#             print(f"Uploading file: {pdf_file.filename} to S3...")
#             s3_client.upload_fileobj(pdf_file, 'your-bucket-name', pdf_file.filename)

#             # Generate a public URL for the uploaded file
#             # file_url = f'https://your-bucket-name.s3.amazonaws.com/{pdf_file.filename}'
#             # Generate a public URL for the uploaded file
#             file_url = f'https://{your-bucket-name}.s3.{your-region}.amazonaws.com/{pdf_file.filename}'

#             print(f"File uploaded successfully. Accessible at: {file_url}")

#             # Extract data from PDF using the file URL
#             print(f"Extracting data from the uploaded PDF...")
#             data = extract_data_from_pdf(file_url)

#             # Create DataFrame and add summary
#             df = pd.DataFrame(data)
#             if not df.empty:
#                 total_sum = df["Total"].sum()
#                 total_orders = len(df)
#                 summary_row = {
#                     "Order ID": "TOTAL SUMMARY",
#                     "Order Date": "",
#                     "Deliver To": "",
#                     "Phone": "",
#                     "Delivery Address": "",
#                     "Total": total_sum
#                 }
#                 df = pd.concat([df, pd.DataFrame([summary_row])], ignore_index=True)

#             # Save DataFrame to Excel and return it as a download
#             output_excel = 'Extracted_Order_Details.xlsx'
#             print(f"Saving data to Excel file: {output_excel}")
#             df.to_excel(output_excel, index=False)

#             # Return the Excel file as a download
#             return send_file(output_excel, as_attachment=True)

#         else:
#             return "Invalid file format. Please upload a PDF.", 400
    
#     except Exception as e:
#         # Log the error message to the console for debugging
#         print(f"Error during file upload and processing: {str(e)}")
#         return f"Internal Server Error: {str(e)}", 500

# def extract_data_from_pdf(pdf_path):
#     try:
#         # Open the PDF file from the given path (in this case, the S3 URL)
#         print(f"Extracting text from PDF at {pdf_path}...")
#         reader = PdfReader(pdf_path)
#         data = []

#         for page in reader.pages:
#             text = page.extract_text()
#             lines = text.split('\n')

#             order_id = ""
#             order_date = ""
#             deliver_to = ""
#             phone = ""
#             delivery_address = ""
#             total = 0.0

#             for idx, line in enumerate(lines):
#                 # ---- Parse Order ID ----
#                 if "Order ID" in line:
#                     match_id = re.search(r"Order ID\s*(\d+)", line)
#                     if match_id:
#                         order_id = match_id.group(1)
#                     else:
#                         if idx + 1 < len(lines):
#                             next_line_match = re.search(r"(\d+)", lines[idx + 1])
#                             if next_line_match:
#                                 order_id = next_line_match.group(1)

#                 # ---- Parse Order Date ----
#                 if "Order Date" in line:
#                     match_date = re.search(r"Order Date:\s*(.*)", line)
#                     if match_date:
#                         order_date = match_date.group(1).strip()
#                     else:
#                         if idx + 1 < len(lines):
#                             order_date = lines[idx + 1].strip()

#                 # ---- Parse Deliver To & Phone ----
#                 if "Deliver To:" in line:
#                     dt_match = re.search(r"Deliver To:\s*(.*)", line)
#                     if dt_match:
#                         dt_str = dt_match.group(1).strip()
#                         phone_match = re.search(r"(?i)phone:\s*(\d+)", dt_str)
#                         if phone_match:
#                             phone = phone_match.group(1)
#                             dt_str = re.sub(r"(?i)phone:\s*\d+", "", dt_str).strip()
#                         deliver_to = dt_str

#                 # ---- Parse Delivery Address ----
#                 if "Delivery Address:" in line:
#                     addr_lines = []
#                     da_match = re.search(r"Delivery Address:\s*(.*)", line)
#                     if da_match:
#                         possible_addr = da_match.group(1).strip()
#                         if possible_addr and not re.search(r'Bill To|Billing Address', possible_addr, re.IGNORECASE):
#                             addr_lines.append(possible_addr)

#                     for j in range(1, 10):
#                         if idx + j < len(lines):
#                             next_line = lines[idx + j].strip()
#                             if "Bill To" in next_line or "Billing Address" in next_line:
#                                 break
#                             addr_lines.append(next_line)
#                         else:
#                             break

#                     delivery_address = ', '.join(addr_lines)

#                 # ---- Parse Total ----
#                 if "Total:" in line:
#                     total_match = re.search(r'Total:\s*([\d,]+\.\d+|\d+)', line)
#                     if total_match:
#                         total = float(total_match.group(1).replace(',', ''))

#             if order_id:
#                 data.append({
#                     "Order ID": order_id,
#                     "Order Date": order_date,
#                     "Deliver To": deliver_to,
#                     "Phone": phone,
#                     "Delivery Address": delivery_address,
#                     "Total": total
#                 })

#         print(f"Successfully extracted {len(data)} records from the PDF.")
#         return data

#     except Exception as e:
#         # Log any errors during PDF extraction
#         print(f"Error extracting data from PDF: {str(e)}")
#         return []

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')











from flask import Flask, render_template, request, send_file
import os
import re
import pandas as pd
from PyPDF2 import PdfReader
import tempfile
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB URI and connection
client = MongoClient('mongodb+srv://ribanapdf:&&Ribana*pdf*2025&&@cluster0.8c12r.mongodb.net/pdf_storage?retryWrites=true&w=majority&tls=true')
db = client['pdf_storage']  # Database name
metadata_collection = db['pdf_metadata']  # Collection name

# Test the connection
try:
    client.admin.command('ping')
    print("Connection successful!")
except Exception as e:
    print("Error:", e)

def index():
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    try:
        if 'pdf_file' not in request.files:
            return "No file part", 400
        
        pdf_file = request.files['pdf_file']

        if pdf_file.filename == '':
            return 'No selected file', 400

        if pdf_file and pdf_file.filename.endswith('.pdf'):
            # Create a temporary file to save the uploaded PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                pdf_file.save(temp_file.name)

                # Extract data from the PDF
                data = extract_data_from_pdf(temp_file.name)

                # Store metadata in MongoDB
                metadata = {
                    'filename': pdf_file.filename,
                    'upload_date': datetime.now(),
                    'file_size': os.path.getsize(temp_file.name),
                    'data_extracted': data,
                }
                metadata_collection.insert_one(metadata)

                # Create DataFrame and add summary
                df = pd.DataFrame(data)
                if not df.empty:
                    total_sum = df["Total"].sum()
                    total_orders = len(df)
                    summary_row = {
                        "Order ID": "TOTAL SUMMARY",
                        "Order Date": "",
                        "Deliver To": "",
                        "Phone": "",
                        "Delivery Address": "",
                        "Total": total_sum
                    }
                    df = pd.concat([df, pd.DataFrame([summary_row])], ignore_index=True)

                # Save DataFrame to Excel and return it as a download
                output_excel = 'Extracted_Order_Details.xlsx'
                df.to_excel(output_excel, index=False)

                os.remove(temp_file.name)  # Remove the temporary file after processing
                return send_file(output_excel, as_attachment=True)

        else:
            return "Invalid file format. Please upload a PDF.", 400
    
    except Exception as e:
        print(f"Error during file upload and processing: {str(e)}")
        return f"Internal Server Error: {str(e)}", 500

def extract_data_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        data = []

        for page in reader.pages:
            text = page.extract_text()
            lines = text.split('\n')

            order_id = ""
            order_date = ""
            deliver_to = ""
            phone = ""
            delivery_address = ""
            total = 0.0

            for idx, line in enumerate(lines):
                # ---- Parse Order ID ----
                if "Order ID" in line:
                    match_id = re.search(r"Order ID\s*(\d+)", line)
                    if match_id:
                        order_id = match_id.group(1)

                # ---- Parse Order Date ----
                if "Order Date" in line:
                    match_date = re.search(r"Order Date:\s*(.*)", line)
                    if match_date:
                        order_date = match_date.group(1).strip()

                # ---- Parse Deliver To & Phone ----
                if "Deliver To:" in line:
                    dt_match = re.search(r"Deliver To:\s*(.*)", line)
                    if dt_match:
                        dt_str = dt_match.group(1).strip()
                        phone_match = re.search(r"(?i)phone:\s*(\d+)", dt_str)
                        if phone_match:
                            phone = phone_match.group(1)
                            dt_str = re.sub(r"(?i)phone:\s*\d+", "", dt_str).strip()
                        deliver_to = dt_str

                # ---- Parse Delivery Address ----
                if "Delivery Address:" in line:
                    addr_lines = []
                    da_match = re.search(r"Delivery Address:\s*(.*)", line)
                    if da_match:
                        possible_addr = da_match.group(1).strip()
                        if possible_addr:
                            addr_lines.append(possible_addr)

                    for j in range(1, 10):
                        if idx + j < len(lines):
                            next_line = lines[idx + j].strip()
                            addr_lines.append(next_line)
                        else:
                            break

                    delivery_address = ', '.join(addr_lines)

                # ---- Parse Total ----
                if "Total:" in line:
                    total_match = re.search(r'Total:\s*([\d,]+\.\d+|\d+)', line)
                    if total_match:
                        total = float(total_match.group(1).replace(',', ''))

            if order_id:
                data.append({
                    "Order ID": order_id,
                    "Order Date": order_date,
                    "Deliver To": deliver_to,
                    "Phone": phone,
                    "Delivery Address": delivery_address,
                    "Total": total
                })

        return data

    except Exception as e:
        print(f"Error extracting data from PDF: {str(e)}")
        return []

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
