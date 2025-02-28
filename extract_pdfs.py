#!/usr/bin/env python3

import mailbox
import os
import email
import sys
from email.header import decode_header
import base64
import quopri
import re

def decode_filename(encoded_filename):
    """Decode filename that might be encoded"""
    if encoded_filename:
        decoded_parts = decode_header(encoded_filename)
        filename_parts = []
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                if encoding:
                    try:
                        filename_parts.append(part.decode(encoding))
                    except:
                        filename_parts.append(part.decode('utf-8', errors='replace'))
                else:
                    filename_parts.append(part.decode('utf-8', errors='replace'))
            else:
                filename_parts.append(part)
        return ''.join(filename_parts)
    return "unknown_filename"

def sanitize_filename(filename):
    """Make the filename safe for the file system"""
    # Replace invalid characters with underscores
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Limit length
    return sanitized[:200]

def extract_pdf_attachments(mbox_path, output_dir):
    """Extract PDF attachments from an mbox file"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"Extracting PDFs from {mbox_path} to {output_dir}")
    
    # Open the mbox file
    mbox = mailbox.mbox(mbox_path)
    
    pdf_count = 0
    email_count = 0
    
    # Process each email in the mbox
    for message in mbox:
        email_count += 1
        if email_count % 100 == 0:
            print(f"Processed {email_count} emails, found {pdf_count} PDFs so far...")
        
        # Get email subject and date for context
        subject = decode_filename(message.get('Subject', 'No Subject'))
        date = message.get('Date', 'No Date')
        
        # Skip the attachment extraction if the message isn't multipart
        if not message.is_multipart():
            continue
        
        # Process all parts of the email
        for part in message.walk():
            content_type = part.get_content_type()
            content_disposition = part.get('Content-Disposition', '')
            
            # Check if this part is a PDF attachment
            is_pdf = False
            if 'application/pdf' in content_type:
                is_pdf = True
            elif content_disposition and 'attachment' in content_disposition:
                filename = part.get_filename()
                if filename and filename.lower().endswith('.pdf'):
                    is_pdf = True
            
            if is_pdf:
                # Get the filename
                filename = part.get_filename()
                if not filename:
                    # If no filename is provided, create one from subject
                    filename = f"{sanitize_filename(subject)}.pdf"
                else:
                    filename = decode_filename(filename)
                    filename = sanitize_filename(filename)
                
                # Add email date to filename to avoid duplicates
                date_str = re.sub(r'[<>:"/\\|?*]', '_', date)
                base, ext = os.path.splitext(filename)
                filename = f"{base}_{date_str}{ext}"
                
                # Get the payload
                payload = part.get_payload(decode=True)
                
                if payload:
                    # Save the attachment
                    file_path = os.path.join(output_dir, filename)
                    with open(file_path, 'wb') as f:
                        f.write(payload)
                    pdf_count += 1
                    print(f"Extracted: {filename}")
    
    print(f"Extraction complete. Found {pdf_count} PDF attachments in {email_count} emails.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_pdfs.py <mbox_file> [output_directory]")
        print("Example: python extract_pdfs.py Sena.mbox extracted_pdfs")
        sys.exit(1)
    
    mbox_path = sys.argv[1]
    # Default output directory is 'extracted_pdfs'
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "extracted_pdfs"
    
    extract_pdf_attachments(mbox_path, output_dir)