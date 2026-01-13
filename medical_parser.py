"""
Medical Prescription Parser
Extracts and organizes medical information from transcribed text
"""
import re
import logging

logger = logging.getLogger(__name__)

def parse_prescription(text):
    """
    Parse medical prescription text and extract:
    - Medicines/Medications
    - Tests/Investigations
    - Patient Description/Problems
    - Dosage Instructions
    """
    text = text.strip()
    
    # Initialize structure
    prescription = {
        'medicines': [],
        'tests': [],
        'patient_description': '',
        'dosage_instructions': [],
        'raw_text': text
    }
    
    # Common medicine patterns (improved to capture medicine names with dosages and forms)
    medicine_patterns = [
        # Pattern: medicine name + dosage (e.g., "omega 20mg", "omeprazole 20 mg")
        r'\b([a-z]+(?:\s+[a-z]+)*)\s+(\d+\s*(?:mg|ml|mcg|g|tablets?|capsules?|drops?|syrup|injection|cream|ointment))\b',
        # Pattern: medicine name + form (e.g., "pelton syrup", "paracetamol tablet")
        r'\b([a-z]+(?:\s+[a-z]+)*)\s+(?:syrup|tablet|capsule|drops?|injection|cream|ointment|gel|spray)\b',
        # Pattern: medicine with common prefixes/suffixes
        r'\b(?:take|prescribe|give|use|apply|medication|medicine|drug)\s+([a-z]+(?:\s+[a-z]+)*(?:\s+\d+\s*(?:mg|ml|mcg|g))?)\b',
    ]
    
    # Test/investigation patterns (improved to capture multi-word test names)
    test_patterns = [
        # Pattern: test keywords + test name (e.g., "abdominal ultrasound", "helicobacter pylori test")
        r'\b(?:test|investigation|check|examine|do|scan|screen|detect)\s+([a-z]+(?:\s+[a-z]+)+)\b',
        # Pattern: test name + test type (e.g., "abdominal ultrasound", "chest x-ray")
        r'\b([a-z]+\s+(?:ultrasound|x-ray|scan|CT scan|MRI|ECG|EKG|blood test|urine test|stool test|culture|biopsy))\b',
        # Pattern: specific test names (multi-word)
        r'\b(helicobacter\s+pylori|h\.?\s*pylori|h\.?\s*p\.?|abdominal\s+ultrasound|chest\s+x-ray|ECG|EKG|CBC|LFT|RFT|KFT|HbA1c|TSH|LDL|HDL|ESR|CRP|CXR|USG|CT|MRI)\b',
        # Pattern: test names with common medical terms
        r'\b([a-z]+\s+(?:test|investigation|scan|screening|examination))\b',
    ]
    
    # Extract tests FIRST (before medicines, to avoid conflicts)
    test_matches = []
    test_names = []
    for pattern in test_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            test = match.group(1).strip()
            if test and len(test) > 2:
                test = ' '.join(test.split())  # Normalize spaces
                # Check if this test is already in the list (case-insensitive)
                if test.lower() not in [t.lower() for t in test_names]:
                    test_matches.append((test, match.start(), match.end()))
                    test_names.append(test)
    
    # Sort by position and add to prescription
    test_matches.sort(key=lambda x: x[1])
    prescription['tests'] = [test for test, _, _ in test_matches]
    
    # Extract medicines
    medicine_matches = []
    for pattern in medicine_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            # Handle patterns with multiple groups (e.g., medicine name + dosage)
            if len(match.groups()) > 1:
                medicine = (match.group(1) + ' ' + match.group(2)).strip()
            else:
                medicine = match.group(1).strip()
            
            if medicine and len(medicine) > 2:
                # Normalize: remove extra spaces
                medicine = ' '.join(medicine.split())
                # Check if this medicine overlaps with any test (to avoid double extraction)
                match_start, match_end = match.span()
                overlaps_with_test = any(start <= match_start < end or start < match_end <= end 
                                        for _, start, end in test_matches)
                if not overlaps_with_test:
                    # Check if this medicine is already in the list (case-insensitive)
                    if not any(m.lower() == medicine.lower() for m, _, _ in medicine_matches):
                        medicine_matches.append((medicine, match_start, match_end))
    
    # Sort by position and add to prescription
    medicine_matches.sort(key=lambda x: x[1])
    prescription['medicines'] = [med for med, _, _ in medicine_matches]
    
    # Extract dosage instructions
    dosage_patterns = [
        r'\b(\d+\s*(?:mg|ml|tablets?|capsules?)?\s*(?:once|twice|thrice|daily|weekly|as needed))',
        r'\b(?:take|give)\s+(\d+\s*(?:tablets?|capsules?|drops?))\s+(?:daily|twice|once)',
    ]
    
    for pattern in dosage_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            dosage = match.group(1).strip()
            if dosage and dosage not in prescription['dosage_instructions']:
                prescription['dosage_instructions'].append(dosage)
    
    # Patient description (remaining text after extracting medicines and tests)
    description_text = text
    # Remove extracted medicines and tests from description
    for medicine in prescription['medicines']:
        description_text = description_text.replace(medicine, '', 1)
    for test in prescription['tests']:
        description_text = description_text.replace(test, '', 1)
    
    prescription['patient_description'] = ' '.join(description_text.split())
    
    logger.info(f"Parsed prescription: {len(prescription['medicines'])} medicines, {len(prescription['tests'])} tests")
    
    return prescription

def format_prescription_html(prescription):
    """Format prescription as HTML - single formatted text box"""
    # Return as plain formatted text wrapped in a div
    formatted_text = format_prescription_text(prescription)
    # Convert newlines to <br> for HTML display
    html_text = formatted_text.replace('\n', '<br>')
    return f'<div class="prescription-formatted-text">{html_text}</div>'

def format_prescription_text(prescription):
    """Format prescription as plain text"""
    text = "MEDICAL PRESCRIPTION\n\n"
    
    # Patient Description
    if prescription['patient_description']:
        text += "PATIENT DESCRIPTION / PROBLEMS:\n"
        text += prescription['patient_description'] + "\n\n"
    
    # Medicines
    if prescription['medicines']:
        text += "MEDICATIONS:\n"
        for i, medicine in enumerate(prescription['medicines'], 1):
            text += f"{i}. {medicine}\n"
        text += "\n"
    
    # Dosage Instructions
    if prescription['dosage_instructions']:
        text += "DOSAGE INSTRUCTIONS:\n"
        for i, dosage in enumerate(prescription['dosage_instructions'], 1):
            text += f"{i}. {dosage}\n"
        text += "\n"
    
    # Tests
    if prescription['tests']:
        text += "TESTS / INVESTIGATIONS:\n"
        for i, test in enumerate(prescription['tests'], 1):
            text += f"{i}. {test}\n"
        text += "\n"
    
    return text

